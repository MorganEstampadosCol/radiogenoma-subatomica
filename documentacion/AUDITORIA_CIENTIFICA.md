# Auditoría científica y de entrega

## Fuentes cotejadas

1. Whaley y Little (1990), [PMID 2371380](https://pubmed.ncbi.nlm.nih.gov/2371380/): TK6/SE30, I-125/I-131, locus HPRT, pendiente `0,45 × 10⁻⁶ por cGy` para I-131 en TK6 y pocas mutaciones en SE30 hasta 38 cGy.
2. Martin y Haseltine (1981), [PMID 7256283](https://pubmed.ncbi.nlm.nih.gov/7256283/): mayor parte del daño radioquímico dentro de 15–20 Å y roturas detectables hasta 70 Å, en el fragmento analizado.
3. LeMotte y Little (1984), [PMID 6704953](https://pubmed.ncbi.nlm.nih.gov/6704953/): fibroblastos humanos y dependencia de condiciones congeladas; sus tasas no se transfieren al simulador.
4. [IAEA TECDOC-1340](https://www-pub.iaea.org/MTCD/publications/PDF/te_1340_web.pdf), [ICRP 137](https://doi.org/10.1177/0146645317734963), [IAEA TECDOC-1608](https://www-pub.iaea.org/MTCD/Publications/PDF/te_1608_web.pdf): modos, semividas y emisiones.
5. [Schmitz et al. (2016), corrección](https://doi.org/10.1016/j.mrgentox.2016.03.003): no equiparar rotura doble y aberración cromosómica; ~250 desintegraciones por aberración en sus nueve experimentos.
6. Diapositivas del curso aportadas por el estudiante: *Decays and scattering* (tasa, actividad, modos, ramificación), *Particle Detection – part 2* (pérdida de energía y alcance). Se conserva la definición positiva `A=−dN/dt`.
7. [O'Neill, Sullivan y Albertini (1990)](https://pubmed.ncbi.nlm.nih.gov/2300074/) y [NCBI Gene, HPRT1](https://www.ncbi.nlm.nih.gov/gene/3251): selección 6-tioguanina y locus HPRT1 humano. Se distingue explícitamente de la deficiencia TK de SE30.

## Comprobaciones reproducibles

`python codigo/verificar.py` pasó 5 controles: semivida y signo de actividad, competencia de salida/decadencia, geometría y criterio de 10 pb, reproducibilidad del Monte Carlo junto con control analítico de la probabilidad de al menos una rotura, conservación de destinos y conversión de unidades HPRT.

`resultados/resumen_modelo.json` documenta tanto el escenario principal de 15.000 eventos por distancia como cuatro barridos de sensibilidad de 6.000 eventos por distancia. Las seis animaciones están en H.264 y la concatenación dura 42 s a 20 fps. El PDF de lectura y la fuente LaTeX se acompañan entre sí; la versión PDF se compuso a partir de la fuente LaTeX con una ruta de exportación alternativa porque la instalación de TeX del entorno no tenía formatos completos.

## Límite científico central

Los datos de Whaley y Little se tomaron de su resumen original verificable. El artículo completo puede requerir acceso institucional. La distribución geométrica de roturas y las tasas celulares son **escenarios explícitos**; su variación con parámetros se muestra para que no se confundan con un ajuste. La extrapolación de 17,1 mutantes por millón a 38 cGy no es una lectura experimental de TK6 a 38 cGy, ni se convierte en riesgo para un individuo. El núcleo hijo nace en el lugar del padre, pero no se presupone que conserve el enlace químico con el ADN después de la desintegración.
