"""Controles físicos y de reproducibilidad (ejecutar: python codigo/verificar.py)."""
import math
import unittest
import numpy as np

from modelo import (T125_D, T131_D, decay_rate, nuclei_remaining,
                    fraction_decay_in_dna, helix, site_probabilities,
                    sample_lesions, score_dsb, lesion_fates,
                    hprt_induced_frequency)


class PhysicalChecks(unittest.TestCase):
    def test_half_lives_and_sign(self):
        for t in (T125_D, T131_D):
            self.assertAlmostEqual(float(nuclei_remaining(100, t, t)),50.)
            self.assertAlmostEqual(decay_rate(t)*t,math.log(2))

    def test_competing_hazards_analytical_limit_and_time(self):
        for t in (T125_D,T131_D):
            p=fraction_decay_in_dna(t,2)
            expected=decay_rate(t)/(decay_rate(t)+.5)
            self.assertAlmostEqual(p,expected)
            self.assertLess(fraction_decay_in_dna(t,2,1),p)
            self.assertAlmostEqual(fraction_decay_in_dna(t,2,0),0)

    def test_geometry_and_operational_double_break(self):
        a,b=helix()
        self.assertAlmostEqual(np.linalg.norm(a[30]-b[30]),2.)
        self.assertAlmostEqual(a[31,2]-a[30,2],.34)
        x=np.zeros(60,bool); y=np.zeros(60,bool)
        x[20]=1;y[30]=1
        self.assertTrue(score_dsb(x,y))
        y[30]=0;y[31]=1
        self.assertFalse(score_dsb(x,y))

    def test_probabilities_and_monte_carlo_seed(self):
        pa,pb=site_probabilities()
        self.assertTrue(np.all((0<=pa)&(pa<1)))
        self.assertGreater(pa[30],pb[30])
        a=sample_lesions(500,(0.,7.),2026)
        b=sample_lesions(500,(0.,7.),2026)
        self.assertEqual(a,b)
        self.assertGreater(a[0]['dsb'],a[1]['dsb'])
        analytic_any=1-float(np.prod(1-pa)*np.prod(1-pb))
        observed=sample_lesions(15000,(0,),2026)[0]['any_break']
        sem=math.sqrt(analytic_any*(1-analytic_any)/15000)
        self.assertLess(abs(observed-analytic_any),4*sem)

    def test_competing_fates_and_units(self):
        t=np.linspace(0,24,25)
        fractions=lesion_fates(t)
        self.assertTrue(np.allclose(sum(fractions),1.))
        self.assertAlmostEqual(float(hprt_induced_frequency(38.)*1e6),17.1)
        self.assertAlmostEqual(float(hprt_induced_frequency(.38*100)),17.1e-6)


if __name__=='__main__':unittest.main(verbosity=2)
