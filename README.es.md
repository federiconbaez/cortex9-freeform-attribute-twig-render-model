# cortex9-freeform-attribute-twig-render-model

Modelo offline e inerte de **CVE-2026-73858** (GHSA-gxrg-x694-283w,
CWE-1336): en Solspace Freeform para Craft CMS 5.0.0-5.10.13,
`Attributes::toHtmlTagArray()` pasaba **todo** valor de atributo no vacío
por el renderizador Twig aislado de Freeform, incluidos `value`, `name` e
`id`, que pueden llevar valores enviados en un formulario. Un `{{ ... }}`
escrito en un formulario público se evaluaba. El fix, commit
`5f7555320635f1cd3b4c478aa0b58e8c3144313b`, omite Twig para esas tres
claves. Está en **5.10.14** (publicada el 2025-05-13; la CVE es del
2026-09-23). Se comprobó antes de construir:
[evidence/fix-in-v5.10.14.md](evidence/fix-in-v5.10.14.md).

Inglés: [README.md](README.md). Ejercicios: [PRACTICE.md](PRACTICE.md).

## El modelo

- `src/c9freeform/attributes.py`: el bucle de `toHtmlTagArray()` antes
  (5f755532:L17 del diff) y después (5f755532:L9, 5f755532:L19-21). Las claves siempre se
  renderizan (5f755532:L16); `empty()` de PHP (`""` y `"0"` nunca se renderizan);
  `in_array` estricto y sensible a mayúsculas.
- `src/c9freeform/twig.py`: un Twig mínimo. `constant()` devuelve
  **marcadores** fijos como `<PHP_VERSION>`; no hay PHP, Twig ni Craft.

## Evidencia diferencial (`results/summary.csv`)

| Clase | n | pre | post |
|---|---|---|---|
| pos | 6 | 5 `TWIG_EVALUATED`, 1 `TWIG_ERROR` | 6 `LITERAL` |
| neg | 5 | 2 evaluados (`class`/`data-*` del admin), 3 literales | igual que pre |
| observación | 1 | `Value` (V mayúscula) evaluado | sigue evaluado |

`o01` es una **observación no verificada** del modelo: nada muestra que
Freeform pase datos enviados bajo esa clave.

## Citas de líneas

Cada cita tiene la forma `<tag>:L<n>` o `<tag>:L<n>-<m>`: la línea real de
`cat -n` del diff upstream del fix. El diff **no** está en este repo
(licencia upstream: Solspace license, LICENSE.md); `sources/diffs.tsv` lo identifica:

- `5f755532` → `CVE-2026-73858_craft-freeform_5f7555320635.diff`, SHA-256 `4f851340fff0d2f88179a1df084530be0415ba8702651a5f50db885bcb6d2c8f`,
  https://github.com/solspace/craft-freeform/commit/5f7555320635f1cd3b4c478aa0b58e8c3144313b.diff

`citations.tsv` es la tabla única de rangos citados; para cada rango guarda
el SHA-256 del texto citado (líneas `start`..`end` del diff tal cual, unidas
con `\n`, sin salto final, UTF-8). Para verificarlo: descargar el diff de la
URL, comprobar su SHA-256 y correr
`C9_DIFF=<ruta> PYTHONPATH=src python3 -m unittest -v tests.test_citations`.
Sin `C9_DIFF` (como en CI) se comprueba el formato, que toda cita esté en la
tabla y que ninguna falte de tag, y el chequeo de contenido sale como
**skip** explícito.

## Uso

```sh
PYTHONPATH=src python3 -m unittest discover -s tests -v
python3 scripts/derive_expected.py | diff - fixtures/expected.tsv
python3 scripts/gen_results.py /tmp/r && diff -r results /tmp/r
```

Un modelo no es un hallazgo. Ver [LIMITATIONS.md](LIMITATIONS.md) y
[SOURCES.md](SOURCES.md). Licencia: Apache-2.0.
