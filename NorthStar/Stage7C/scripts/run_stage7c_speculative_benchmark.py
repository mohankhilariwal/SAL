#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from northstar_compliance.inference.speculative import MarkovModel, expected_acceptance_probability, kl_divergence, speculative_sample, verify_empirical_distribution_parity

def main()->int:
    p=argparse.ArgumentParser(); p.add_argument('--trials',type=int,default=20000); p.add_argument('--tokens',type=int,default=128); args=p.parse_args()
    target=MarkovModel({'A':.58,'B':.32,'C':.10},{'A':{'A':.65,'B':.25,'C':.10},'B':{'A':.30,'B':.55,'C':.15},'C':{'A':.45,'B':.25,'C':.30}})
    draft=MarkovModel({'A':.53,'B':.34,'C':.13},{'A':{'A':.59,'B':.28,'C':.13},'B':{'A':.34,'B':.49,'C':.17},'C':{'A':.41,'B':.28,'C':.31}})
    parity,tv=verify_empirical_distribution_parity(target,draft,trials=args.trials,tolerance=.025,seed=17)
    trace=speculative_sample(target,draft,max_tokens=args.tokens,speculative_tokens=4,seed=23)
    payload={'evidence_kind':'simulated','lossless_algorithm':'draft-target rejection correction','parity_passed':parity,'total_variation_distance':tv,'acceptance_rate':trace.acceptance_rate,'mean_tokens_per_target_step':trace.mean_tokens_per_target_step,'proposed_tokens':trace.proposed_tokens,'accepted_tokens':trace.accepted_tokens,'rejected_tokens':trace.rejected_tokens,'start_acceptance_probability':expected_acceptance_probability(target.start,draft.start),'start_kl_divergence':kl_divergence(target.start,draft.start),'warning':'This validates toy distribution semantics, not GPU speed or NorthStar production benefit.'}
    print(json.dumps(payload,indent=2)); return 0 if parity else 2
if __name__=='__main__': raise SystemExit(main())
