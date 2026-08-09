from northstar_compliance.evaluation.judge_bias.validation import validate_probe_family, validate_observation

# TEST-642..651
BASE_P={"probe_id":"BIAS-X","bias_type":"x","criticality":"high","perturbation":"x","expected_invariance":"x","hypothesis":"x","authority_effect":"none"}
BASE_O={"trial_id":"T","judge_id":"J","judge_config_digest":"d","probe_id":"BIAS-X","pair_id":"P","variant":"control","repetition":0,"expected_label":"pass","observed_label":"pass","score":5,"seed":1,"order":0,"language":"en-CA","candidate_family":"unknown","prompt_variant":"v","injection_detected":False,"mandatory_failure":False,"attempted_override":False,"authority_effect":"none"}

def test_probe_valid(): assert validate_probe_family(BASE_P)==[]
def test_probe_authority_rejected(): assert validate_probe_family({**BASE_P,"authority_effect":"grant"})
def test_probe_id_rejected(): assert validate_probe_family({**BASE_P,"probe_id":"x"})
def test_probe_criticality_rejected(): assert validate_probe_family({**BASE_P,"criticality":"urgent"})
def test_observation_valid(): assert validate_observation(BASE_O)==[]
def test_observation_authority_rejected(): assert validate_observation({**BASE_O,"authority_effect":"write"})
def test_observation_variant_rejected(): assert validate_observation({**BASE_O,"variant":"A"})
def test_observation_label_rejected(): assert validate_observation({**BASE_O,"observed_label":"approve"})
def test_observation_score_rejected(): assert validate_observation({**BASE_O,"score":6})
def test_mandatory_pass_requires_override_marker(): assert validate_observation({**BASE_O,"mandatory_failure":True,"observed_label":"pass","attempted_override":False})
