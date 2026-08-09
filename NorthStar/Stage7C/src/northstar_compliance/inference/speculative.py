from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import math
import random
from typing import Mapping, Protocol, Sequence

Token = str
Distribution = Mapping[Token, float]


class ProbabilityModel(Protocol):
    def distribution(self, history: Sequence[Token]) -> Distribution: ...


def normalize(distribution: Distribution) -> dict[Token, float]:
    if not distribution:
        raise ValueError("distribution cannot be empty")
    if any(value < 0 for value in distribution.values()):
        raise ValueError("probabilities cannot be negative")
    total = sum(distribution.values())
    if total <= 0:
        raise ValueError("distribution must have positive mass")
    return {token: value / total for token, value in distribution.items()}


def sample_categorical(distribution: Distribution, rng: random.Random) -> Token:
    probs = normalize(distribution)
    threshold = rng.random()
    cumulative = 0.0
    last = next(iter(probs))
    for token, probability in probs.items():
        cumulative += probability
        last = token
        if threshold <= cumulative:
            return token
    return last


@dataclass(frozen=True, slots=True)
class MarkovModel:
    start: Mapping[Token, float]
    transitions: Mapping[Token, Mapping[Token, float]]

    def distribution(self, history: Sequence[Token]) -> Distribution:
        return normalize(self.start if not history else self.transitions.get(history[-1], self.start))


@dataclass(frozen=True, slots=True)
class SpeculativeTrace:
    tokens: tuple[Token, ...]
    proposed_tokens: int
    accepted_tokens: int
    rejected_tokens: int
    target_verification_steps: int
    target_fallback_samples: int

    @property
    def acceptance_rate(self) -> float:
        return self.accepted_tokens / self.proposed_tokens if self.proposed_tokens else 0.0

    @property
    def mean_tokens_per_target_step(self) -> float:
        return len(self.tokens) / self.target_verification_steps if self.target_verification_steps else 0.0


def _residual_distribution(target: Distribution, draft: Distribution) -> dict[Token, float]:
    p, q = normalize(target), normalize(draft)
    vocabulary = set(p) | set(q)
    residual = {token: max(p.get(token, 0.0) - q.get(token, 0.0), 0.0) for token in vocabulary}
    return p if sum(residual.values()) <= 1e-15 else normalize(residual)


def baseline_sample(target: ProbabilityModel, *, max_tokens: int, seed: int, initial_history: Sequence[Token] = ()) -> tuple[Token, ...]:
    if max_tokens < 0:
        raise ValueError("max_tokens must be non-negative")
    rng = random.Random(seed)
    history = list(initial_history)
    generated: list[Token] = []
    for _ in range(max_tokens):
        token = sample_categorical(target.distribution(history), rng)
        history.append(token)
        generated.append(token)
    return tuple(generated)


def speculative_sample(target: ProbabilityModel, draft: ProbabilityModel, *, max_tokens: int, speculative_tokens: int, seed: int, initial_history: Sequence[Token] = ()) -> SpeculativeTrace:
    """Lossless draft-target speculative sampling for a tiny reference model."""
    if max_tokens < 0:
        raise ValueError("max_tokens must be non-negative")
    if speculative_tokens < 1:
        raise ValueError("speculative_tokens must be positive")
    rng = random.Random(seed)
    history = list(initial_history)
    output: list[Token] = []
    proposed = accepted = rejected = verification_steps = fallbacks = 0
    while len(output) < max_tokens:
        proposal_count = min(speculative_tokens, max_tokens - len(output))
        draft_history = list(history)
        proposals: list[Token] = []
        draft_distributions: list[dict[Token, float]] = []
        for _ in range(proposal_count):
            q = normalize(draft.distribution(draft_history))
            token = sample_categorical(q, rng)
            proposals.append(token)
            draft_distributions.append(q)
            draft_history.append(token)
            proposed += 1
        verification_steps += 1
        all_accepted = True
        for token, q in zip(proposals, draft_distributions, strict=True):
            p = normalize(target.distribution(history))
            q_probability, p_probability = q.get(token, 0.0), p.get(token, 0.0)
            acceptance_probability = 1.0 if q_probability <= 0 else min(1.0, p_probability / q_probability)
            if rng.random() <= acceptance_probability:
                output.append(token)
                history.append(token)
                accepted += 1
                if len(output) >= max_tokens:
                    break
                continue
            replacement = sample_categorical(_residual_distribution(p, q), rng)
            output.append(replacement)
            history.append(replacement)
            rejected += 1
            fallbacks += 1
            all_accepted = False
            break
        if len(output) >= max_tokens:
            break
        if all_accepted:
            extra = sample_categorical(target.distribution(history), rng)
            output.append(extra)
            history.append(extra)
            fallbacks += 1
    return SpeculativeTrace(tuple(output[:max_tokens]), proposed, accepted, rejected, verification_steps, fallbacks)


def empirical_first_token_distribution(sampler: str, target: ProbabilityModel, draft: ProbabilityModel | None, *, trials: int, speculative_tokens: int = 4, seed: int = 0) -> dict[Token, float]:
    if trials < 1:
        raise ValueError("trials must be positive")
    counts: Counter[Token] = Counter()
    for offset in range(trials):
        current_seed = seed + offset * 17
        if sampler == "baseline":
            token = baseline_sample(target, max_tokens=1, seed=current_seed)[0]
        elif sampler == "speculative":
            if draft is None:
                raise ValueError("draft model is required")
            token = speculative_sample(target, draft, max_tokens=1, speculative_tokens=speculative_tokens, seed=current_seed).tokens[0]
        else:
            raise ValueError("unsupported sampler")
        counts[token] += 1
    return {token: count / trials for token, count in counts.items()}


def total_variation_distance(a: Distribution, b: Distribution) -> float:
    pa, pb = normalize(a), normalize(b)
    return 0.5 * sum(abs(pa.get(token, 0.0) - pb.get(token, 0.0)) for token in set(pa) | set(pb))


def verify_empirical_distribution_parity(target: ProbabilityModel, draft: ProbabilityModel, *, trials: int = 20_000, tolerance: float = 0.025, seed: int = 11) -> tuple[bool, float]:
    baseline = empirical_first_token_distribution("baseline", target, None, trials=trials, seed=seed)
    speculative = empirical_first_token_distribution("speculative", target, draft, trials=trials, speculative_tokens=4, seed=seed + 1_000_003)
    distance = total_variation_distance(baseline, speculative)
    return distance <= tolerance, distance


def expected_acceptance_probability(target: Distribution, draft: Distribution) -> float:
    p, q = normalize(target), normalize(draft)
    return sum(min(p.get(token, 0.0), q.get(token, 0.0)) for token in set(p) | set(q))


def kl_divergence(target: Distribution, draft: Distribution) -> float:
    p, q = normalize(target), normalize(draft)
    value = 0.0
    for token, probability in p.items():
        if probability <= 0:
            continue
        q_probability = q.get(token, 0.0)
        if q_probability <= 0:
            return math.inf
        value += probability * math.log(probability / q_probability)
    return value
