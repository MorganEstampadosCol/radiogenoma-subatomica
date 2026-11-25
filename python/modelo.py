"""Modelo pedagogico reproducible de radionuclidos en ADN humano.

Ninguna tasa de lesion/reparacion aqui se ajusta a pacientes. Los parametros
ilustrativos se mantienen separados de los datos experimentales publicados.
"""
from __future__ import annotations

import numpy as np

T125_D = 59.4  # IAEA TECDOC-1340
T131_D = 8.021  # ICRP 137
SLOPE_HPRT_PER_CGY = 0.45e-6  # Whaley & Little, 1990, TK6, 131IUdR
R_DNA_NM = 1.0  # geometria B-ADN esquematica, no estructura atomistica
PITCH_NM = 3.4


def decay_rate(half_life_days: float) -> float:
    if half_life_days <= 0:
        raise ValueError("semivida positiva")
    return np.log(2.0) / half_life_days


def nuclei_remaining(n0: float, t_days, half_life_days: float):
    if n0 < 0:
        raise ValueError("n0 no puede ser negativo")
    return n0 * np.exp(-decay_rate(half_life_days) * np.asarray(t_days))


def fraction_decay_in_dna(half_life_days: float, residence_days: float,
                          t_days: float = np.inf) -> float:
    """Riesgos competitivos: desintegracion y salida celular exponenciales.

    residence_days = tiempo medio de salida, no semivida biologica.
    """
    if residence_days <= 0 or t_days < 0:
        raise ValueError("tiempos fisicos positivos")
    lam = decay_rate(half_life_days)
    k = 1.0 / residence_days
    return float(lam / (lam + k) * (-np.expm1(-(lam + k) * t_days)))


def helix(n_bp: int = 60):
    """Dos espinas de azucar-fosfato ideales; 10 pb por vuelta ilustrativa."""
    if n_bp < 11:
        raise ValueError("la ventana debe incluir al menos una vuelta")
    j = np.arange(n_bp)
    angle = 2 * np.pi * (j - n_bp // 2) / 10
    z = (j - n_bp // 2) * (PITCH_NM / 10)
    a = np.column_stack((R_DNA_NM * np.cos(angle), R_DNA_NM * np.sin(angle), z))
    b = np.column_stack((-a[:, 0], -a[:, 1], z))
    return a, b


def site_probabilities(offset_nm: float = 0., opportunity: float = 0.48,
                       length_nm: float = 1.5, n_bp: int = 60):
    """P(SSB_j)=1-exp[-mu exp(-r_j/ell)]; hipotesis, no espectro Auger.

    El origen (1+offset,0,0) representa una fuente sobre el exterior de la
    hebra A al offset=0. Los perfiles no reproducen datos de Martin 1981.
    """
    if offset_nm < 0 or opportunity < 0 or length_nm <= 0:
        raise ValueError("parametros fuera de dominio")
    a, b = helix(n_bp)
    source = np.array([R_DNA_NM + offset_nm, 0., 0.])
    d_a = np.linalg.norm(a - source, axis=1)
    d_b = np.linalg.norm(b - source, axis=1)
    return (1 - np.exp(-opportunity * np.exp(-d_a / length_nm)),
            1 - np.exp(-opportunity * np.exp(-d_b / length_nm)))


def score_dsb(a_breaks, b_breaks, max_separation_bp=10):
    """Al menos un par de roturas opuestas separado <= 10 pb (criterio operativo)."""
    ia = np.flatnonzero(a_breaks)
    ib = np.flatnonzero(b_breaks)
    return bool(len(ia) and len(ib) and np.any(np.abs(ia[:, None] - ib) <= max_separation_bp))


def sample_lesions(n_events=15000, offsets=(0, 1, 2, 4, 7), seed=2026,
                   opportunity=0.48, length_nm=1.5):
    """Ensamble de eventos condicionados a UN decaimiento y fuente fija.

    El uso de numeros comunes mejora la comparacion entre escenarios.
    Retorna medias, error estandar binomial y frecuencias SSB/DSB.
    """
    if n_events <= 0:
        raise ValueError("n_events debe ser positivo")
    rng = np.random.default_rng(seed)
    u = rng.random((2, n_events, 60))
    out = []
    for offset in offsets:
        pa, pb = site_probabilities(float(offset), opportunity, length_nm)
        ba, bb = u[0] < pa, u[1] < pb
        any_break = np.any(ba | bb, axis=1)
        # 10 bp: union de desplazamientos; bordes fuera de la ventana no cuentan.
        pair = np.zeros(n_events, dtype=bool)
        for shift in range(-10, 11):
            if shift >= 0:
                pair |= np.any(ba[:, :60-shift] & bb[:, shift:], axis=1)
            else:
                pair |= np.any(ba[:, -shift:] & bb[:, :60+shift], axis=1)
        p = float(pair.mean())
        out.append(dict(offset_nm=float(offset), any_break=float(any_break.mean()),
                        dsb=p, sem=float(np.sqrt(p * (1 - p) / n_events)),
                        events=int(n_events)))
    return out


def lesion_fates(t_hours, kr=0.20, km=0.02, kd=0.03):
    """Estado inicial L=1; reparacion, fijacion y perdida son competidores."""
    if min(kr, km, kd) < 0 or kr + km + kd <= 0:
        raise ValueError("tasas no negativas y al menos una positiva")
    t = np.asarray(t_hours)
    if np.any(t < 0):
        raise ValueError("tiempo no negativo")
    K = kr + km + kd
    remaining = np.exp(-K * t)
    processed = -np.expm1(-K * t)
    return remaining, kr / K * processed, km / K * processed, kd / K * processed


def hprt_induced_frequency(dose_cgy):
    d = np.asarray(dose_cgy)
    if np.any(d < 0):
        raise ValueError("dosis no negativa")
    return SLOPE_HPRT_PER_CGY * d


def illustrative_hprt_counts(dose_cgy=38., cells=1_000_000, background=10e-6,
                             repetitions=5000, seed=2026):
    if cells <= 0 or background < 0:
        raise ValueError("celulas positivas y fondo no negativo")
    rng = np.random.default_rng(seed)
    ctrl = rng.poisson(cells * background, repetitions)
    treated = rng.poisson(cells * (background + float(hprt_induced_frequency(dose_cgy))), repetitions)
    return ctrl, treated


if __name__ == "__main__":
    import json
    from pathlib import Path
    out = Path(__file__).resolve().parents[1] / "resultados"
    out.mkdir(exist_ok=True)
    results = {"fuentes": {"I125_days": T125_D, "I131_days": T131_D,
                            "TK6_131I_HPRT_induced_per_cGy": SLOPE_HPRT_PER_CGY},
               "escenario_dna": sample_lesions(),
               "sensibilidad_modelo": {
                   "mu_0_24": sample_lesions(6000, (0, 4), opportunity=.24),
                   "mu_0_96": sample_lesions(6000, (0, 4), opportunity=.96),
                   "ell_1_0_nm": sample_lesions(6000, (0, 4), length_nm=1.0),
                   "ell_2_0_nm": sample_lesions(6000, (0, 4), length_nm=2.0)},
               "retencion_hipotetica_2dias": {
                   "I125": fraction_decay_in_dna(T125_D, 2.),
                   "I131": fraction_decay_in_dna(T131_D, 2.)},
               "extrapolacion_TK6_38cGy_por_millon": float(hprt_induced_frequency(38.) * 1e6)}
    (out / "resumen_modelo.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
