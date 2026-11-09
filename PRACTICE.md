# Guía práctica (7 niveles)

Ejercicios **offline** sobre inyección de plantillas en atributos. Los
payloads son marcadores inertes que solo evalúa el modelo local. Úsalos en
tu máquina o en tu propio laboratorio (por ejemplo, un Craft CMS con
Freeform en una VM tuya), nunca contra sitios de terceros. Respuestas en
`tests/test_practice.py`.

Ayuda: `PYTHONPATH=src python3 -c "from c9freeform import attributes as a; print(a.evaluate('pre', [('value', '{{ 7*7 }}')], {}))"`.

**Básico**

1. **Twig legítimo del admin.** `class = "f-{{ h }}"` con `h = "x"`.
   (`f-x` en pre y post)
2. **El valor enviado, antes.** `value = "{{ 7*7 }}"` en pre. (`49`)

**Intermedio**

3. **El valor enviado, después.** Lo mismo en post. (literal)
4. **Constantes.** `{{ constant('PHP_OS') }}` en `value`. (pre
   `<PHP_OS>`, post literal) ¿Qué tipo de dato revelaría en un sistema real?
5. **Errores de render.** `value = "{{ 7*"` en pre. (`TWIG_ERROR`)

**Avanzado**

6. **`empty()` de PHP.** `value = "0"`: ¿por qué no se renderiza ni antes
   ni después?
7. **Lo que el fix no cubre.** `data-n = "{{ 7*7 }}"` en post sigue dando
   `49`. ¿Es un problema? Solo si llegan datos del usuario a esa clave, y
   eso **no está verificado**.

Más allá: agrega un caso a `fixtures/cases.json`, regenera
`fixtures/expected.tsv` con `scripts/derive_expected.py` y comprueba que
coinciden.
