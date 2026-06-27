import reward_config_onlywar as ow
import reward_config_annihilation as an


def _const_keys(mod):
    return {k for k in vars(mod) if k.isupper() and not k.startswith("_")}


def test_shared_keys_identical_between_profiles():
    mission_specific = {k for k in _const_keys(an) if k.startswith("ANNIHILATION_")}
    shared_annihilation = _const_keys(an) - mission_specific
    shared_only_war = _const_keys(ow)
    missing_in_annihilation = shared_only_war - shared_annihilation
    extra_in_annihilation = shared_annihilation - shared_only_war
    assert not missing_in_annihilation, f"Ключи есть в onlywar, нет в annihilation: {missing_in_annihilation}"
    assert not extra_in_annihilation, f"Лишние общие ключи в annihilation: {extra_in_annihilation}"


def test_shared_keys_types_match():
    """Совпадение типов shared keys (кроме mission-specific ANNIHILATION_*)."""
    mission_specific = {k for k in _const_keys(an) if k.startswith("ANNIHILATION_")}
    shared = _const_keys(ow) & (_const_keys(an) - mission_specific)
    mismatches = []
    for k in sorted(shared):
        ow_type = type(getattr(ow, k))
        an_type = type(getattr(an, k))
        if ow_type is not an_type:
            mismatches.append(f"{k}: onlywar={ow_type.__name__} annihilation={an_type.__name__}")
    assert not mismatches, f"Несовпадение типов shared keys: {mismatches}"
