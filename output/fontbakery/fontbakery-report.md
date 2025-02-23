## FontBakery report

fontbakery version: 0.13.2





## Experimental checks

These won't break the CI job for now, but will become effective after some time if nobody raises any concern.


<details><summary>[1] Giphurs-Regular.otf</summary>
<div>
<details>
    <summary>🔥 <b>FAIL</b> Check base characters have non-zero advance width. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#base-has-width">base_has_width</a></summary>
    <div>







* 🔥 **FAIL** <p>The following glyphs had zero advance width:
- uni0488 (U+0488)</p>
<pre><code>- uni0489 (U+0489)
</code></pre>
 [code: zero-width-bases]



</div>
</details>
</div>
</details>

<details><summary>[1] GiphursExtraBlack-Regular.otf</summary>
<div>
<details>
    <summary>🔥 <b>FAIL</b> Check base characters have non-zero advance width. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#base-has-width">base_has_width</a></summary>
    <div>







* 🔥 **FAIL** <p>The following glyphs had zero advance width:
- uni0488 (U+0488)</p>
<pre><code>- uni0489 (U+0489)
</code></pre>
 [code: zero-width-bases]



</div>
</details>
</div>
</details>




## All other checks



<details><summary>[1] Family checks</summary>
<div>
<details>
    <summary>🔥 <b>FAIL</b> Verify that family names in the name table are consistent across all fonts in the family. Checks Typographic Family name (nameID 16) if present, otherwise uses Font Family name (nameID 1) <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.html#opentype-family-consistent-family-name">opentype/family/consistent_family_name</a></summary>
    <div>







* 🔥 **FAIL** <p>2 different Font Family names were found:</p>
<ul>
<li>
<p>'Giphurs' was found in:</p>
<ul>
<li>Giphurs-Regular.otf (nameID 1)</li>
</ul>
</li>
<li>
<p>'Giphurs ExtraBlack' was found in:</p>
<ul>
<li>GiphursExtraBlack-Regular.otf (nameID 1)</li>
</ul>
</li>
</ul>
 [code: inconsistent-family-name]



</div>
</details>
</div>
</details>

<details><summary>[9] Giphurs-Regular.otf</summary>
<div>
<details>
    <summary>💥 <b>ERROR</b> Shapes languages in all GF glyphsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-glyphsets-shape-languages">googlefonts/glyphsets/shape_languages</a></summary>
    <div>







* 💥 **ERROR** <p>Failed with TypeError: argument 'lang': 'NoneType' object cannot be converted to 'Language'</p>
<pre><code>  File &quot;/media/corne2plum3/Users/corne/Fonts/- My Fonts/Giphurs/venv/lib/python3.12/site-packages/fontbakery/checkrunner.py&quot;, line 222, in _run_check
    subresults = list(subresults)
                 ^^^^^^^^^^^^^^^^
  File &quot;/media/corne2plum3/Users/corne/Fonts/- My Fonts/Giphurs/venv/lib/python3.12/site-packages/fontbakery/checks/vendorspecific/googlefonts/glyphsets/shape_languages.py&quot;, line 49, in check_glyphsets_shape_languages
    reporter = shaperglot_checker.check(shaperglot_languages[language_code])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

</code></pre>
 [code: failed-check]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check GDEF mark glyph class doesn't have characters that are not marks. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.html#opentype-gdef-non-mark-chars">opentype/gdef_non_mark_chars</a></summary>
    <div>







* ⚠️ **WARN** <p>The following non-mark characters should not be in the GDEF mark glyph class:
U+0384, U+0385, U+1FBD, U+1FBE, U+1FBF, U+1FC0, U+1FC1, U+1FCD, U+1FCE, U+1FCF, U+1FDD, U+1FDE, U+1FDF, U+1FED, U+1FEE, U+1FEF, U+1FFD and U+1FFE</p>
 [code: non-mark-chars]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check glyphs in mark glyph class are non-spacing. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.html#opentype-gdef-spacing-marks">opentype/gdef_spacing_marks</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs seem to be spacing (because they have width &gt; 0 on the hmtx table) so they may be in the GDEF mark glyph class by mistake, or they should have zero width instead:
dieresistonos (U+0385), tonos (U+0384), tonos2 (unencoded), uni1FBD (U+1FBD), uni1FBE (U+1FBE), uni1FBF (U+1FBF), uni1FC0 (U+1FC0), uni1FC1 (U+1FC1), uni1FCD (U+1FCD), uni1FCE (U+1FCE), uni1FCF (U+1FCF), uni1FDD (U+1FDD), uni1FDE (U+1FDE), uni1FDF (U+1FDF), uni1FED (U+1FED), uni1FEE (U+1FEE), uni1FEF (U+1FEF), uni1FFD (U+1FFD) and uni1FFE (U+1FFE)</p>
 [code: spacing-mark-glyphs]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#unreachable-glyphs">unreachable_glyphs</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs could not be reached by codepoint or substitution rules:</p>
<pre><code>- acutecomb.case

- acutecomb_uni0307

- double_circle_empty

- gravecomb.case

- tildecomb.case

- tildecomb_uni0308.case

- tonos2

- uni0302.case

- uni0304.case

- uni0306.case

- uni0306_acutecomb.case

- uni0306_gravecomb.case

- uni0306_hookabovecomb.case

- uni0307.case

- uni0308.case

- uni030B.case

- uni030C.case

- uni030C_uni0307.case

- uni030F.case
</code></pre>
 [code: unreachable-glyphs]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Validate size, and resolution of article images, and ensure article page has minimum length and includes visual assets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-article-images">googlefonts/article/images</a></summary>
    <div>







* ⚠️ **WARN** <p>Family metadata at fonts/otf does not have an article.</p>
 [code: lacks-article]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-metadata-unreachable-subsetting">googlefonts/metadata/unreachable_subsetting</a></summary>
    <div>







* ⚠️ **WARN** <p>The following codepoints supported by the font are not covered by
any subsets defined in the font's metadata file, and will never
be served. You can solve this by either manually adding additional
subset declarations to METADATA.pb, or by editing the glyphset
definitions.</p>
<ul>
<li>U+02CD MODIFIER LETTER LOW MACRON: try adding lisu</li>
<li>U+02D8 BREVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DB OGONEK: try adding one of: canadian-aboriginal, yi</li>
<li>U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: tifinagh, coptic, math, cherokee</li>
<li>U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh</li>
<li>U+0307 COMBINING DOT ABOVE: try adding one of: old-permic, syriac, tifinagh, coptic, malayalam, math, tai-le, todhri, canadian-aboriginal, hebrew, duployan</li>
<li>U+030A COMBINING RING ABOVE: try adding one of: syriac, duployan</li>
<li>U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage</li>
<li>U+030C COMBINING CARON: try adding one of: tai-le, cherokee</li>
<li>U+030D COMBINING VERTICAL LINE ABOVE: try adding sunuwar</li>
<li>U+030F COMBINING DOUBLE GRAVE ACCENT: not included in any glyphset definition</li>
<li>U+0311 COMBINING INVERTED BREVE: try adding one of: coptic, todhri</li>
<li>U+0312 COMBINING TURNED COMMA ABOVE: try adding math</li>
<li>U+0313 COMBINING COMMA ABOVE: try adding one of: old-permic, todhri</li>
<li>U+0314 COMBINING REVERSED COMMA ABOVE: not included in any glyphset definition</li>
<li>U+0315 COMBINING COMMA ABOVE RIGHT: try adding math</li>
<li>U+031B COMBINING HORN: not included in any glyphset definition</li>
<li>U+0324 COMBINING DIAERESIS BELOW: try adding one of: syriac, duployan, cherokee</li>
<li>U+0325 COMBINING RING BELOW: try adding syriac</li>
<li>U+0326 COMBINING COMMA BELOW: try adding math</li>
<li>U+0327 COMBINING CEDILLA: try adding math</li>
<li>U+0328 COMBINING OGONEK: not included in any glyphset definition</li>
<li>U+032D COMBINING CIRCUMFLEX ACCENT BELOW: try adding one of: syriac, sunuwar</li>
<li>U+032E COMBINING BREVE BELOW: try adding syriac</li>
<li>U+032F COMBINING INVERTED BREVE BELOW: try adding math</li>
<li>U+0330 COMBINING TILDE BELOW: try adding one of: syriac, math, cherokee</li>
<li>U+0331 COMBINING MACRON BELOW: try adding one of: thai, syriac, gothic, sunuwar, tifinagh, cherokee, caucasian-albanian</li>
<li>U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+0338 COMBINING LONG SOLIDUS OVERLAY: try adding math</li>
<li>U+0340 COMBINING GRAVE TONE MARK: not included in any glyphset definition</li>
<li>U+0341 COMBINING ACUTE TONE MARK: not included in any glyphset definition</li>
<li>U+0342 COMBINING GREEK PERISPOMENI: not included in any glyphset definition</li>
<li>U+0343 COMBINING GREEK KORONIS: not included in any glyphset definition</li>
<li>U+0345 COMBINING GREEK YPOGEGRAMMENI: not included in any glyphset definition</li>
<li>U+0357 COMBINING RIGHT HALF RING ABOVE: not included in any glyphset definition</li>
<li>U+035F COMBINING DOUBLE MACRON BELOW: not included in any glyphset definition</li>
<li>U+1DC4 COMBINING MACRON-ACUTE: not included in any glyphset definition</li>
<li>U+1DC5 COMBINING GRAVE-MACRON: not included in any glyphset definition</li>
<li>U+1DC6 COMBINING MACRON-GRAVE: not included in any glyphset definition</li>
<li>U+1DC7 COMBINING ACUTE-MACRON: not included in any glyphset definition</li>
<li>U+2010 HYPHEN: try adding one of: kharoshthi, syloti-nagri, lisu, kaithi, armenian, coptic, sundanese, cham, sora-sompeng, arabic, hebrew, yi, kayah-li</li>
<li>U+2011 NON-BREAKING HYPHEN: try adding one of: arabic, syloti-nagri, yi</li>
<li>U+2012 FIGURE DASH: not included in any glyphset definition</li>
<li>U+2015 HORIZONTAL BAR: try adding adlam</li>
<li>U+2016 DOUBLE VERTICAL LINE: try adding math</li>
<li>U+2017 DOUBLE LOW LINE: try adding math</li>
<li>U+201B SINGLE HIGH-REVERSED-9 QUOTATION MARK: try adding adlam</li>
<li>U+201F DOUBLE HIGH-REVERSED-9 QUOTATION MARK: not included in any glyphset definition</li>
<li>U+2021 DOUBLE DAGGER: try adding adlam</li>
<li>U+2023 TRIANGULAR BULLET: not included in any glyphset definition</li>
<li>U+2024 ONE DOT LEADER: try adding armenian</li>
<li>U+2025 TWO DOT LEADER: try adding phags-pa</li>
<li>U+2027 HYPHENATION POINT: not included in any glyphset definition</li>
<li>U+2030 PER MILLE SIGN: try adding adlam</li>
<li>U+2031 PER TEN THOUSAND SIGN: not included in any glyphset definition</li>
<li>U+2034 TRIPLE PRIME: try adding math</li>
<li>U+2035 REVERSED PRIME: try adding math</li>
<li>U+2036 REVERSED DOUBLE PRIME: try adding math</li>
<li>U+2037 REVERSED TRIPLE PRIME: try adding math</li>
<li>U+2038 CARET: try adding math</li>
<li>U+203B REFERENCE MARK: not included in any glyphset definition</li>
<li>U+203C DOUBLE EXCLAMATION MARK: try adding math</li>
<li>U+203D INTERROBANG: not included in any glyphset definition</li>
<li>U+203E OVERLINE: not included in any glyphset definition</li>
<li>U+203F UNDERTIE: not included in any glyphset definition</li>
<li>U+2040 CHARACTER TIE: try adding math</li>
<li>U+2041 CARET INSERTION POINT: not included in any glyphset definition</li>
<li>U+2042 ASTERISM: not included in any glyphset definition</li>
<li>U+2043 HYPHEN BULLET: try adding math</li>
<li>U+2045 LEFT SQUARE BRACKET WITH QUILL: not included in any glyphset definition</li>
<li>U+2046 RIGHT SQUARE BRACKET WITH QUILL: not included in any glyphset definition</li>
<li>U+2047 DOUBLE QUESTION MARK: try adding math</li>
<li>U+2048 QUESTION EXCLAMATION MARK: try adding mongolian</li>
<li>U+2049 EXCLAMATION QUESTION MARK: try adding mongolian</li>
<li>U+204A TIRONIAN SIGN ET: not included in any glyphset definition</li>
<li>U+204B REVERSED PILCROW SIGN: not included in any glyphset definition</li>
<li>U+204C BLACK LEFTWARDS BULLET: not included in any glyphset definition</li>
<li>U+204D BLACK RIGHTWARDS BULLET: not included in any glyphset definition</li>
<li>U+204E LOW ASTERISK: not included in any glyphset definition</li>
<li>U+204F REVERSED SEMICOLON: try adding one of: arabic, adlam</li>
<li>U+2050 CLOSE UP: try adding math</li>
<li>U+2051 TWO ASTERISKS ALIGNED VERTICALLY: not included in any glyphset definition</li>
<li>U+2052 COMMERCIAL MINUS SIGN: not included in any glyphset definition</li>
<li>U+2053 SWUNG DASH: try adding coptic</li>
<li>U+2054 INVERTED UNDERTIE: not included in any glyphset definition</li>
<li>U+2055 FLOWER PUNCTUATION MARK: try adding syloti-nagri</li>
<li>U+2056 THREE DOT PUNCTUATION: try adding coptic</li>
<li>U+2057 QUADRUPLE PRIME: try adding math</li>
<li>U+2058 FOUR DOT PUNCTUATION: try adding coptic</li>
<li>U+2059 FIVE DOT PUNCTUATION: try adding coptic</li>
<li>U+205A TWO DOT PUNCTUATION: try adding one of: old-turkic, carian, georgian, glagolitic, lycian, old-hungarian</li>
<li>U+205B FOUR DOT MARK: not included in any glyphset definition</li>
<li>U+205C DOTTED CROSS: not included in any glyphset definition</li>
<li>U+205D TRICOLON: try adding one of: carian, meroitic-hieroglyphs, old-hungarian, meroitic</li>
<li>U+205E VERTICAL FOUR DOTS: try adding old-hungarian</li>
<li>U+2070 SUPERSCRIPT ZERO: try adding math</li>
<li>U+2071 SUPERSCRIPT LATIN SMALL LETTER I: try adding math</li>
<li>U+2074 SUPERSCRIPT FOUR: try adding math</li>
<li>U+2075 SUPERSCRIPT FIVE: try adding math</li>
<li>U+2076 SUPERSCRIPT SIX: try adding math</li>
<li>U+2077 SUPERSCRIPT SEVEN: try adding math</li>
<li>U+2078 SUPERSCRIPT EIGHT: try adding math</li>
<li>U+2079 SUPERSCRIPT NINE: try adding math</li>
<li>U+207A SUPERSCRIPT PLUS SIGN: try adding math</li>
<li>U+207B SUPERSCRIPT MINUS: try adding math</li>
<li>U+207C SUPERSCRIPT EQUALS SIGN: try adding math</li>
<li>U+207D SUPERSCRIPT LEFT PARENTHESIS: try adding math</li>
<li>U+207E SUPERSCRIPT RIGHT PARENTHESIS: try adding math</li>
<li>U+207F SUPERSCRIPT LATIN SMALL LETTER N: try adding math</li>
<li>U+2080 SUBSCRIPT ZERO: try adding math</li>
<li>U+2081 SUBSCRIPT ONE: try adding math</li>
<li>U+2082 SUBSCRIPT TWO: try adding math</li>
<li>U+2083 SUBSCRIPT THREE: try adding math</li>
<li>U+2084 SUBSCRIPT FOUR: try adding math</li>
<li>U+2085 SUBSCRIPT FIVE: try adding math</li>
<li>U+2086 SUBSCRIPT SIX: try adding math</li>
<li>U+2087 SUBSCRIPT SEVEN: try adding math</li>
<li>U+2088 SUBSCRIPT EIGHT: try adding math</li>
<li>U+2089 SUBSCRIPT NINE: try adding math</li>
<li>U+208A SUBSCRIPT PLUS SIGN: try adding math</li>
<li>U+208B SUBSCRIPT MINUS: try adding math</li>
<li>U+208C SUBSCRIPT EQUALS SIGN: try adding math</li>
<li>U+208D SUBSCRIPT LEFT PARENTHESIS: try adding math</li>
<li>U+208E SUBSCRIPT RIGHT PARENTHESIS: try adding math</li>
<li>U+2090 LATIN SUBSCRIPT SMALL LETTER A: try adding math</li>
<li>U+2091 LATIN SUBSCRIPT SMALL LETTER E: try adding math</li>
<li>U+2092 LATIN SUBSCRIPT SMALL LETTER O: try adding math</li>
<li>U+2093 LATIN SUBSCRIPT SMALL LETTER X: try adding math</li>
<li>U+2094 LATIN SUBSCRIPT SMALL LETTER SCHWA: try adding math</li>
<li>U+2095 LATIN SUBSCRIPT SMALL LETTER H: try adding math</li>
<li>U+2096 LATIN SUBSCRIPT SMALL LETTER K: try adding math</li>
<li>U+2097 LATIN SUBSCRIPT SMALL LETTER L: try adding math</li>
<li>U+2098 LATIN SUBSCRIPT SMALL LETTER M: try adding math</li>
<li>U+2099 LATIN SUBSCRIPT SMALL LETTER N: try adding math</li>
<li>U+209A LATIN SUBSCRIPT SMALL LETTER P: try adding math</li>
<li>U+209B LATIN SUBSCRIPT SMALL LETTER S: try adding math</li>
<li>U+209C LATIN SUBSCRIPT SMALL LETTER T: try adding math</li>
<li>U+2100 ACCOUNT OF: try adding math</li>
<li>U+2101 ADDRESSED TO THE SUBJECT: try adding math</li>
<li>U+2102 DOUBLE-STRUCK CAPITAL C: try adding math</li>
<li>U+2103 DEGREE CELSIUS: try adding math</li>
<li>U+2104 CENTRE LINE SYMBOL: try adding math</li>
<li>U+2105 CARE OF: try adding math</li>
<li>U+2106 CADA UNA: try adding math</li>
<li>U+2107 EULER CONSTANT: try adding math</li>
<li>U+2108 SCRUPLE: try adding math</li>
<li>U+2109 DEGREE FAHRENHEIT: try adding math</li>
<li>U+210A SCRIPT SMALL G: try adding math</li>
<li>U+210B SCRIPT CAPITAL H: try adding math</li>
<li>U+210C BLACK-LETTER CAPITAL H: try adding math</li>
<li>U+210D DOUBLE-STRUCK CAPITAL H: try adding math</li>
<li>U+210E PLANCK CONSTANT: try adding math</li>
<li>U+210F PLANCK CONSTANT OVER TWO PI: try adding math</li>
<li>U+2110 SCRIPT CAPITAL I: try adding math</li>
<li>U+2111 BLACK-LETTER CAPITAL I: try adding math</li>
<li>U+2112 SCRIPT CAPITAL L: try adding math</li>
<li>U+2114 L B BAR SYMBOL: try adding math</li>
<li>U+2115 DOUBLE-STRUCK CAPITAL N: try adding math</li>
<li>U+2117 SOUND RECORDING COPYRIGHT: try adding math</li>
<li>U+2118 SCRIPT CAPITAL P: try adding math</li>
<li>U+2119 DOUBLE-STRUCK CAPITAL P: try adding math</li>
<li>U+211A DOUBLE-STRUCK CAPITAL Q: try adding math</li>
<li>U+211B SCRIPT CAPITAL R: try adding math</li>
<li>U+211C BLACK-LETTER CAPITAL R: try adding math</li>
<li>U+211D DOUBLE-STRUCK CAPITAL R: try adding math</li>
<li>U+211E PRESCRIPTION TAKE: try adding math</li>
<li>U+211F RESPONSE: try adding math</li>
<li>U+2120 SERVICE MARK: try adding math</li>
<li>U+2121 TELEPHONE SIGN: try adding math</li>
<li>U+2123 VERSICLE: try adding math</li>
<li>U+2124 DOUBLE-STRUCK CAPITAL Z: try adding math</li>
<li>U+2125 OUNCE SIGN: try adding math</li>
<li>U+2126 OHM SIGN: try adding math</li>
<li>U+2127 INVERTED OHM SIGN: try adding math</li>
<li>U+2128 BLACK-LETTER CAPITAL Z: try adding math</li>
<li>U+2129 TURNED GREEK SMALL LETTER IOTA: try adding math</li>
<li>U+212A KELVIN SIGN: try adding math</li>
<li>U+212B ANGSTROM SIGN: try adding math</li>
<li>U+212C SCRIPT CAPITAL B: try adding math</li>
<li>U+212D BLACK-LETTER CAPITAL C: try adding math</li>
<li>U+212E ESTIMATED SYMBOL: try adding math</li>
<li>U+212F SCRIPT SMALL E: try adding math</li>
<li>U+2130 SCRIPT CAPITAL E: try adding math</li>
<li>U+2131 SCRIPT CAPITAL F: try adding math</li>
<li>U+2132 TURNED CAPITAL F: try adding math</li>
<li>U+2133 SCRIPT CAPITAL M: try adding math</li>
<li>U+2134 SCRIPT SMALL O: try adding math</li>
<li>U+2135 ALEF SYMBOL: try adding math</li>
<li>U+2136 BET SYMBOL: try adding math</li>
<li>U+2137 GIMEL SYMBOL: try adding math</li>
<li>U+2138 DALET SYMBOL: try adding math</li>
<li>U+2139 INFORMATION SOURCE: try adding math</li>
<li>U+213A ROTATED CAPITAL Q: try adding math</li>
<li>U+213B FACSIMILE SIGN: try adding math</li>
<li>U+213C DOUBLE-STRUCK SMALL PI: try adding math</li>
<li>U+213D DOUBLE-STRUCK SMALL GAMMA: try adding math</li>
<li>U+213E DOUBLE-STRUCK CAPITAL GAMMA: try adding math</li>
<li>U+213F DOUBLE-STRUCK CAPITAL PI: try adding math</li>
<li>U+2140 DOUBLE-STRUCK N-ARY SUMMATION: try adding math</li>
<li>U+2141 TURNED SANS-SERIF CAPITAL G: try adding math</li>
<li>U+2142 TURNED SANS-SERIF CAPITAL L: try adding math</li>
<li>U+2143 REVERSED SANS-SERIF CAPITAL L: try adding math</li>
<li>U+2144 TURNED SANS-SERIF CAPITAL Y: try adding math</li>
<li>U+2145 DOUBLE-STRUCK ITALIC CAPITAL D: try adding math</li>
<li>U+2146 DOUBLE-STRUCK ITALIC SMALL D: try adding math</li>
<li>U+2147 DOUBLE-STRUCK ITALIC SMALL E: try adding math</li>
<li>U+2148 DOUBLE-STRUCK ITALIC SMALL I: try adding math</li>
<li>U+2149 DOUBLE-STRUCK ITALIC SMALL J: try adding math</li>
<li>U+214A PROPERTY LINE: try adding math</li>
<li>U+214B TURNED AMPERSAND: try adding math</li>
<li>U+214C PER SIGN: try adding math</li>
<li>U+214D AKTIESELSKAB: try adding math</li>
<li>U+214E TURNED SMALL F: try adding math</li>
<li>U+214F SYMBOL FOR SAMARITAN SOURCE: try adding math</li>
<li>U+2150 VULGAR FRACTION ONE SEVENTH: try adding symbols</li>
<li>U+2151 VULGAR FRACTION ONE NINTH: try adding symbols</li>
<li>U+2152 VULGAR FRACTION ONE TENTH: try adding symbols</li>
<li>U+2153 VULGAR FRACTION ONE THIRD: try adding symbols</li>
<li>U+2154 VULGAR FRACTION TWO THIRDS: try adding symbols</li>
<li>U+2155 VULGAR FRACTION ONE FIFTH: try adding symbols</li>
<li>U+2156 VULGAR FRACTION TWO FIFTHS: try adding symbols</li>
<li>U+2157 VULGAR FRACTION THREE FIFTHS: try adding symbols</li>
<li>U+2158 VULGAR FRACTION FOUR FIFTHS: try adding symbols</li>
<li>U+2159 VULGAR FRACTION ONE SIXTH: try adding symbols</li>
<li>U+215A VULGAR FRACTION FIVE SIXTHS: try adding symbols</li>
<li>U+215B VULGAR FRACTION ONE EIGHTH: try adding symbols</li>
<li>U+215C VULGAR FRACTION THREE EIGHTHS: try adding symbols</li>
<li>U+215D VULGAR FRACTION FIVE EIGHTHS: try adding symbols</li>
<li>U+215E VULGAR FRACTION SEVEN EIGHTHS: try adding symbols</li>
<li>U+215F FRACTION NUMERATOR ONE: try adding symbols</li>
<li>U+2160 ROMAN NUMERAL ONE: try adding symbols</li>
<li>U+2161 ROMAN NUMERAL TWO: try adding symbols</li>
<li>U+2162 ROMAN NUMERAL THREE: try adding symbols</li>
<li>U+2163 ROMAN NUMERAL FOUR: try adding symbols</li>
<li>U+2164 ROMAN NUMERAL FIVE: try adding symbols</li>
<li>U+2165 ROMAN NUMERAL SIX: try adding symbols</li>
<li>U+2166 ROMAN NUMERAL SEVEN: try adding symbols</li>
<li>U+2167 ROMAN NUMERAL EIGHT: try adding symbols</li>
<li>U+2168 ROMAN NUMERAL NINE: try adding symbols</li>
<li>U+2169 ROMAN NUMERAL TEN: try adding symbols</li>
<li>U+216A ROMAN NUMERAL ELEVEN: try adding symbols</li>
<li>U+216B ROMAN NUMERAL TWELVE: try adding symbols</li>
<li>U+216C ROMAN NUMERAL FIFTY: try adding symbols</li>
<li>U+216D ROMAN NUMERAL ONE HUNDRED: try adding symbols</li>
<li>U+216E ROMAN NUMERAL FIVE HUNDRED: try adding symbols</li>
<li>U+216F ROMAN NUMERAL ONE THOUSAND: try adding symbols</li>
<li>U+2170 SMALL ROMAN NUMERAL ONE: try adding symbols</li>
<li>U+2171 SMALL ROMAN NUMERAL TWO: try adding symbols</li>
<li>U+2172 SMALL ROMAN NUMERAL THREE: try adding symbols</li>
<li>U+2173 SMALL ROMAN NUMERAL FOUR: try adding symbols</li>
<li>U+2174 SMALL ROMAN NUMERAL FIVE: try adding symbols</li>
<li>U+2175 SMALL ROMAN NUMERAL SIX: try adding symbols</li>
<li>U+2176 SMALL ROMAN NUMERAL SEVEN: try adding symbols</li>
<li>U+2177 SMALL ROMAN NUMERAL EIGHT: try adding symbols</li>
<li>U+2178 SMALL ROMAN NUMERAL NINE: try adding symbols</li>
<li>U+2179 SMALL ROMAN NUMERAL TEN: try adding symbols</li>
<li>U+217A SMALL ROMAN NUMERAL ELEVEN: try adding symbols</li>
<li>U+217B SMALL ROMAN NUMERAL TWELVE: try adding symbols</li>
<li>U+217C SMALL ROMAN NUMERAL FIFTY: try adding symbols</li>
<li>U+217D SMALL ROMAN NUMERAL ONE HUNDRED: try adding symbols</li>
<li>U+217E SMALL ROMAN NUMERAL FIVE HUNDRED: try adding symbols</li>
<li>U+217F SMALL ROMAN NUMERAL ONE THOUSAND: try adding symbols</li>
<li>U+2180 ROMAN NUMERAL ONE THOUSAND C D: try adding symbols</li>
<li>U+2181 ROMAN NUMERAL FIVE THOUSAND: try adding symbols</li>
<li>U+2182 ROMAN NUMERAL TEN THOUSAND: try adding symbols</li>
<li>U+2183 ROMAN NUMERAL REVERSED ONE HUNDRED: try adding symbols</li>
<li>U+2184 LATIN SMALL LETTER REVERSED C: not included in any glyphset definition</li>
<li>U+2185 ROMAN NUMERAL SIX LATE FORM: try adding symbols</li>
<li>U+2186 ROMAN NUMERAL FIFTY EARLY FORM: try adding symbols</li>
<li>U+2187 ROMAN NUMERAL FIFTY THOUSAND: try adding symbols</li>
<li>U+2188 ROMAN NUMERAL ONE HUNDRED THOUSAND: try adding symbols</li>
<li>U+2189 VULGAR FRACTION ZERO THIRDS: try adding symbols</li>
<li>U+218A TURNED DIGIT TWO: try adding symbols</li>
<li>U+218B TURNED DIGIT THREE: try adding symbols</li>
<li>U+2190 LEFTWARDS ARROW: try adding one of: symbols, math</li>
<li>U+2192 RIGHTWARDS ARROW: try adding one of: symbols, math</li>
<li>U+2194 LEFT RIGHT ARROW: try adding one of: symbols, math</li>
<li>U+2195 UP DOWN ARROW: try adding one of: symbols, math</li>
<li>U+2196 NORTH WEST ARROW: try adding one of: symbols, math</li>
<li>U+2197 NORTH EAST ARROW: try adding one of: symbols, math</li>
<li>U+2198 SOUTH EAST ARROW: try adding one of: symbols, math</li>
<li>U+2199 SOUTH WEST ARROW: try adding one of: symbols, math</li>
<li>U+219A LEFTWARDS ARROW WITH STROKE: try adding math</li>
<li>U+219B RIGHTWARDS ARROW WITH STROKE: try adding math</li>
<li>U+219C LEFTWARDS WAVE ARROW: try adding math</li>
<li>U+219D RIGHTWARDS WAVE ARROW: try adding math</li>
<li>U+219E LEFTWARDS TWO HEADED ARROW: try adding math</li>
<li>U+219F UPWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A0 RIGHTWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A1 DOWNWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A2 LEFTWARDS ARROW WITH TAIL: try adding math</li>
<li>U+21A3 RIGHTWARDS ARROW WITH TAIL: try adding math</li>
<li>U+21A4 LEFTWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A5 UPWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A6 RIGHTWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A7 DOWNWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A8 UP DOWN ARROW WITH BASE: try adding math</li>
<li>U+21A9 LEFTWARDS ARROW WITH HOOK: try adding math</li>
<li>U+21AA RIGHTWARDS ARROW WITH HOOK: try adding math</li>
<li>U+21AB LEFTWARDS ARROW WITH LOOP: try adding math</li>
<li>U+21AC RIGHTWARDS ARROW WITH LOOP: try adding math</li>
<li>U+21AD LEFT RIGHT WAVE ARROW: try adding math</li>
<li>U+21AE LEFT RIGHT ARROW WITH STROKE: try adding math</li>
<li>U+21AF DOWNWARDS ZIGZAG ARROW: try adding symbols</li>
<li>U+21B0 UPWARDS ARROW WITH TIP LEFTWARDS: try adding math</li>
<li>U+21B1 UPWARDS ARROW WITH TIP RIGHTWARDS: try adding math</li>
<li>U+21B2 DOWNWARDS ARROW WITH TIP LEFTWARDS: try adding math</li>
<li>U+21B3 DOWNWARDS ARROW WITH TIP RIGHTWARDS: try adding math</li>
<li>U+21B4 RIGHTWARDS ARROW WITH CORNER DOWNWARDS: try adding math</li>
<li>U+21B5 DOWNWARDS ARROW WITH CORNER LEFTWARDS: try adding math</li>
<li>U+21B6 ANTICLOCKWISE TOP SEMICIRCLE ARROW: try adding math</li>
<li>U+21B7 CLOCKWISE TOP SEMICIRCLE ARROW: try adding math</li>
<li>U+21B8 NORTH WEST ARROW TO LONG BAR: try adding math</li>
<li>U+21B9 LEFTWARDS ARROW TO BAR OVER RIGHTWARDS ARROW TO BAR: try adding math</li>
<li>U+21BA ANTICLOCKWISE OPEN CIRCLE ARROW: try adding math</li>
<li>U+21BB CLOCKWISE OPEN CIRCLE ARROW: try adding math</li>
<li>U+21BC LEFTWARDS HARPOON WITH BARB UPWARDS: try adding math</li>
<li>U+21BD LEFTWARDS HARPOON WITH BARB DOWNWARDS: try adding math</li>
<li>U+21BE UPWARDS HARPOON WITH BARB RIGHTWARDS: try adding math</li>
<li>U+21BF UPWARDS HARPOON WITH BARB LEFTWARDS: try adding math</li>
<li>U+21C0 RIGHTWARDS HARPOON WITH BARB UPWARDS: try adding math</li>
<li>U+21C1 RIGHTWARDS HARPOON WITH BARB DOWNWARDS: try adding math</li>
<li>U+21C2 DOWNWARDS HARPOON WITH BARB RIGHTWARDS: try adding math</li>
<li>U+21C3 DOWNWARDS HARPOON WITH BARB LEFTWARDS: try adding math</li>
<li>U+21C4 RIGHTWARDS ARROW OVER LEFTWARDS ARROW: try adding math</li>
<li>U+21C5 UPWARDS ARROW LEFTWARDS OF DOWNWARDS ARROW: try adding math</li>
<li>U+21C6 LEFTWARDS ARROW OVER RIGHTWARDS ARROW: try adding math</li>
<li>U+21C7 LEFTWARDS PAIRED ARROWS: try adding math</li>
<li>U+21C8 UPWARDS PAIRED ARROWS: try adding math</li>
<li>U+21C9 RIGHTWARDS PAIRED ARROWS: try adding math</li>
<li>U+21CA DOWNWARDS PAIRED ARROWS: try adding math</li>
<li>U+21CB LEFTWARDS HARPOON OVER RIGHTWARDS HARPOON: try adding math</li>
<li>U+21CC RIGHTWARDS HARPOON OVER LEFTWARDS HARPOON: try adding math</li>
<li>U+21CD LEFTWARDS DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21CE LEFT RIGHT DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21CF RIGHTWARDS DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21D0 LEFTWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D1 UPWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D2 RIGHTWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D3 DOWNWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D4 LEFT RIGHT DOUBLE ARROW: try adding math</li>
<li>U+21D5 UP DOWN DOUBLE ARROW: try adding math</li>
<li>U+21D6 NORTH WEST DOUBLE ARROW: try adding math</li>
<li>U+21D7 NORTH EAST DOUBLE ARROW: try adding math</li>
<li>U+21D8 SOUTH EAST DOUBLE ARROW: try adding math</li>
<li>U+21D9 SOUTH WEST DOUBLE ARROW: try adding math</li>
<li>U+21DA LEFTWARDS TRIPLE ARROW: try adding math</li>
<li>U+21DB RIGHTWARDS TRIPLE ARROW: try adding math</li>
<li>U+21DC LEFTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+21DD RIGHTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+21DE UPWARDS ARROW WITH DOUBLE STROKE: try adding math</li>
<li>U+21DF DOWNWARDS ARROW WITH DOUBLE STROKE: try adding math</li>
<li>U+21E0 LEFTWARDS DASHED ARROW: try adding math</li>
<li>U+21E1 UPWARDS DASHED ARROW: try adding math</li>
<li>U+21E2 RIGHTWARDS DASHED ARROW: try adding math</li>
<li>U+21E3 DOWNWARDS DASHED ARROW: try adding math</li>
<li>U+21E4 LEFTWARDS ARROW TO BAR: try adding math</li>
<li>U+21E5 RIGHTWARDS ARROW TO BAR: try adding math</li>
<li>U+21E6 LEFTWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E7 UPWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E8 RIGHTWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E9 DOWNWARDS WHITE ARROW: try adding symbols</li>
<li>U+21EA UPWARDS WHITE ARROW FROM BAR: try adding symbols</li>
<li>U+21EB UPWARDS WHITE ARROW ON PEDESTAL: try adding symbols</li>
<li>U+21EC UPWARDS WHITE ARROW ON PEDESTAL WITH HORIZONTAL BAR: try adding symbols</li>
<li>U+21ED UPWARDS WHITE ARROW ON PEDESTAL WITH VERTICAL BAR: try adding symbols</li>
<li>U+21EE UPWARDS WHITE DOUBLE ARROW: try adding symbols</li>
<li>U+21EF UPWARDS WHITE DOUBLE ARROW ON PEDESTAL: try adding symbols</li>
<li>U+21F0 RIGHTWARDS WHITE ARROW FROM WALL: try adding symbols</li>
<li>U+21F1 NORTH WEST ARROW TO CORNER: try adding math</li>
<li>U+21F2 SOUTH EAST ARROW TO CORNER: try adding math</li>
<li>U+21F3 UP DOWN WHITE ARROW: try adding symbols</li>
<li>U+21F4 RIGHT ARROW WITH SMALL CIRCLE: try adding math</li>
<li>U+21F5 DOWNWARDS ARROW LEFTWARDS OF UPWARDS ARROW: try adding math</li>
<li>U+21F6 THREE RIGHTWARDS ARROWS: try adding math</li>
<li>U+21F7 LEFTWARDS ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21F8 RIGHTWARDS ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21F9 LEFT RIGHT ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21FA LEFTWARDS ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FB RIGHTWARDS ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FC LEFT RIGHT ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FD LEFTWARDS OPEN-HEADED ARROW: try adding math</li>
<li>U+21FE RIGHTWARDS OPEN-HEADED ARROW: try adding math</li>
<li>U+21FF LEFT RIGHT OPEN-HEADED ARROW: try adding math</li>
<li>U+2200 FOR ALL: try adding math</li>
<li>U+2201 COMPLEMENT: try adding math</li>
<li>U+2202 PARTIAL DIFFERENTIAL: try adding math</li>
<li>U+2203 THERE EXISTS: try adding math</li>
<li>U+2204 THERE DOES NOT EXIST: try adding math</li>
<li>U+2205 EMPTY SET: try adding math</li>
<li>U+2206 INCREMENT: try adding math</li>
<li>U+2207 NABLA: try adding math</li>
<li>U+2208 ELEMENT OF: try adding math</li>
<li>U+2209 NOT AN ELEMENT OF: try adding math</li>
<li>U+220A SMALL ELEMENT OF: try adding math</li>
<li>U+220B CONTAINS AS MEMBER: try adding math</li>
<li>U+220C DOES NOT CONTAIN AS MEMBER: try adding math</li>
<li>U+220D SMALL CONTAINS AS MEMBER: try adding math</li>
<li>U+220E END OF PROOF: try adding math</li>
<li>U+220F N-ARY PRODUCT: try adding math</li>
<li>U+2210 N-ARY COPRODUCT: try adding math</li>
<li>U+2211 N-ARY SUMMATION: try adding math</li>
<li>U+2213 MINUS-OR-PLUS SIGN: try adding math</li>
<li>U+2214 DOT PLUS: try adding math</li>
<li>U+2216 SET MINUS: try adding math</li>
<li>U+2217 ASTERISK OPERATOR: try adding math</li>
<li>U+2218 RING OPERATOR: try adding one of: symbols, math</li>
<li>U+2219 BULLET OPERATOR: try adding one of: tai-tham, symbols, math, yi</li>
<li>U+221A SQUARE ROOT: try adding math</li>
<li>U+221B CUBE ROOT: try adding math</li>
<li>U+221C FOURTH ROOT: try adding math</li>
<li>U+221D PROPORTIONAL TO: try adding math</li>
<li>U+221E INFINITY: try adding math</li>
<li>U+221F RIGHT ANGLE: try adding math</li>
<li>U+2220 ANGLE: try adding math</li>
<li>U+2221 MEASURED ANGLE: try adding math</li>
<li>U+2222 SPHERICAL ANGLE: try adding math</li>
<li>U+2223 DIVIDES: try adding math</li>
<li>U+2224 DOES NOT DIVIDE: try adding math</li>
<li>U+2225 PARALLEL TO: try adding math</li>
<li>U+2226 NOT PARALLEL TO: try adding math</li>
<li>U+2227 LOGICAL AND: try adding math</li>
<li>U+2228 LOGICAL OR: try adding math</li>
<li>U+2229 INTERSECTION: try adding math</li>
<li>U+222A UNION: try adding math</li>
<li>U+222B INTEGRAL: try adding math</li>
<li>U+222C DOUBLE INTEGRAL: try adding math</li>
<li>U+222D TRIPLE INTEGRAL: try adding math</li>
<li>U+222E CONTOUR INTEGRAL: try adding math</li>
<li>U+222F SURFACE INTEGRAL: try adding math</li>
<li>U+2230 VOLUME INTEGRAL: try adding math</li>
<li>U+2231 CLOCKWISE INTEGRAL: try adding math</li>
<li>U+2232 CLOCKWISE CONTOUR INTEGRAL: try adding math</li>
<li>U+2233 ANTICLOCKWISE CONTOUR INTEGRAL: try adding math</li>
<li>U+2234 THEREFORE: try adding math</li>
<li>U+2235 BECAUSE: try adding math</li>
<li>U+2236 RATIO: try adding math</li>
<li>U+2237 PROPORTION: try adding math</li>
<li>U+2238 DOT MINUS: try adding math</li>
<li>U+2239 EXCESS: try adding math</li>
<li>U+223A GEOMETRIC PROPORTION: try adding math</li>
<li>U+223B HOMOTHETIC: try adding math</li>
<li>U+223C TILDE OPERATOR: try adding math</li>
<li>U+223D REVERSED TILDE: try adding math</li>
<li>U+223E INVERTED LAZY S: try adding math</li>
<li>U+223F SINE WAVE: try adding math</li>
<li>U+2240 WREATH PRODUCT: try adding math</li>
<li>U+2241 NOT TILDE: try adding math</li>
<li>U+2242 MINUS TILDE: try adding math</li>
<li>U+2243 ASYMPTOTICALLY EQUAL TO: try adding math</li>
<li>U+2244 NOT ASYMPTOTICALLY EQUAL TO: try adding math</li>
<li>U+2245 APPROXIMATELY EQUAL TO: try adding math</li>
<li>U+2246 APPROXIMATELY BUT NOT ACTUALLY EQUAL TO: try adding math</li>
<li>U+2247 NEITHER APPROXIMATELY NOR ACTUALLY EQUAL TO: try adding math</li>
<li>U+2248 ALMOST EQUAL TO: try adding math</li>
<li>U+2249 NOT ALMOST EQUAL TO: try adding math</li>
<li>U+224A ALMOST EQUAL OR EQUAL TO: try adding math</li>
<li>U+224B TRIPLE TILDE: try adding math</li>
<li>U+224C ALL EQUAL TO: try adding math</li>
<li>U+224D EQUIVALENT TO: try adding math</li>
<li>U+224E GEOMETRICALLY EQUIVALENT TO: try adding math</li>
<li>U+224F DIFFERENCE BETWEEN: try adding math</li>
<li>U+2250 APPROACHES THE LIMIT: try adding math</li>
<li>U+2251 GEOMETRICALLY EQUAL TO: try adding math</li>
<li>U+2252 APPROXIMATELY EQUAL TO OR THE IMAGE OF: try adding math</li>
<li>U+2253 IMAGE OF OR APPROXIMATELY EQUAL TO: try adding math</li>
<li>U+2254 COLON EQUALS: try adding math</li>
<li>U+2255 EQUALS COLON: try adding math</li>
<li>U+2256 RING IN EQUAL TO: try adding math</li>
<li>U+2257 RING EQUAL TO: try adding math</li>
<li>U+2258 CORRESPONDS TO: try adding math</li>
<li>U+2259 ESTIMATES: try adding math</li>
<li>U+225A EQUIANGULAR TO: try adding math</li>
<li>U+225B STAR EQUALS: try adding math</li>
<li>U+225C DELTA EQUAL TO: try adding math</li>
<li>U+225D EQUAL TO BY DEFINITION: try adding math</li>
<li>U+225E MEASURED BY: try adding math</li>
<li>U+225F QUESTIONED EQUAL TO: try adding math</li>
<li>U+2260 NOT EQUAL TO: try adding math</li>
<li>U+2261 IDENTICAL TO: try adding math</li>
<li>U+2262 NOT IDENTICAL TO: try adding math</li>
<li>U+2263 STRICTLY EQUIVALENT TO: try adding math</li>
<li>U+2264 LESS-THAN OR EQUAL TO: try adding math</li>
<li>U+2265 GREATER-THAN OR EQUAL TO: try adding math</li>
<li>U+2266 LESS-THAN OVER EQUAL TO: try adding math</li>
<li>U+2267 GREATER-THAN OVER EQUAL TO: try adding math</li>
<li>U+2268 LESS-THAN BUT NOT EQUAL TO: try adding math</li>
<li>U+2269 GREATER-THAN BUT NOT EQUAL TO: try adding math</li>
<li>U+226A MUCH LESS-THAN: try adding math</li>
<li>U+226B MUCH GREATER-THAN: try adding math</li>
<li>U+226C BETWEEN: try adding math</li>
<li>U+226D NOT EQUIVALENT TO: try adding math</li>
<li>U+226E NOT LESS-THAN: try adding math</li>
<li>U+226F NOT GREATER-THAN: try adding math</li>
<li>U+2270 NEITHER LESS-THAN NOR EQUAL TO: try adding math</li>
<li>U+2271 NEITHER GREATER-THAN NOR EQUAL TO: try adding math</li>
<li>U+2272 LESS-THAN OR EQUIVALENT TO: try adding math</li>
<li>U+2273 GREATER-THAN OR EQUIVALENT TO: try adding math</li>
<li>U+2274 NEITHER LESS-THAN NOR EQUIVALENT TO: try adding math</li>
<li>U+2275 NEITHER GREATER-THAN NOR EQUIVALENT TO: try adding math</li>
<li>U+2276 LESS-THAN OR GREATER-THAN: try adding math</li>
<li>U+2277 GREATER-THAN OR LESS-THAN: try adding math</li>
<li>U+2278 NEITHER LESS-THAN NOR GREATER-THAN: try adding math</li>
<li>U+2279 NEITHER GREATER-THAN NOR LESS-THAN: try adding math</li>
<li>U+227A PRECEDES: try adding math</li>
<li>U+227B SUCCEEDS: try adding math</li>
<li>U+227C PRECEDES OR EQUAL TO: try adding math</li>
<li>U+227D SUCCEEDS OR EQUAL TO: try adding math</li>
<li>U+227E PRECEDES OR EQUIVALENT TO: try adding math</li>
<li>U+227F SUCCEEDS OR EQUIVALENT TO: try adding math</li>
<li>U+2280 DOES NOT PRECEDE: try adding math</li>
<li>U+2281 DOES NOT SUCCEED: try adding math</li>
<li>U+2282 SUBSET OF: try adding math</li>
<li>U+2283 SUPERSET OF: try adding math</li>
<li>U+2284 NOT A SUBSET OF: try adding math</li>
<li>U+2285 NOT A SUPERSET OF: try adding math</li>
<li>U+2286 SUBSET OF OR EQUAL TO: try adding math</li>
<li>U+2287 SUPERSET OF OR EQUAL TO: try adding math</li>
<li>U+2288 NEITHER A SUBSET OF NOR EQUAL TO: try adding math</li>
<li>U+2289 NEITHER A SUPERSET OF NOR EQUAL TO: try adding math</li>
<li>U+228A SUBSET OF WITH NOT EQUAL TO: try adding math</li>
<li>U+228B SUPERSET OF WITH NOT EQUAL TO: try adding math</li>
<li>U+228C MULTISET: try adding math</li>
<li>U+228D MULTISET MULTIPLICATION: try adding math</li>
<li>U+228E MULTISET UNION: try adding math</li>
<li>U+228F SQUARE IMAGE OF: try adding math</li>
<li>U+2290 SQUARE ORIGINAL OF: try adding math</li>
<li>U+2291 SQUARE IMAGE OF OR EQUAL TO: try adding math</li>
<li>U+2292 SQUARE ORIGINAL OF OR EQUAL TO: try adding math</li>
<li>U+2293 SQUARE CAP: try adding math</li>
<li>U+2294 SQUARE CUP: try adding math</li>
<li>U+2295 CIRCLED PLUS: try adding math</li>
<li>U+2296 CIRCLED MINUS: try adding math</li>
<li>U+2297 CIRCLED TIMES: try adding math</li>
<li>U+2298 CIRCLED DIVISION SLASH: try adding math</li>
<li>U+2299 CIRCLED DOT OPERATOR: try adding one of: symbols, math</li>
<li>U+229A CIRCLED RING OPERATOR: try adding math</li>
<li>U+229B CIRCLED ASTERISK OPERATOR: try adding math</li>
<li>U+229C CIRCLED EQUALS: try adding math</li>
<li>U+229D CIRCLED DASH: try adding math</li>
<li>U+229E SQUARED PLUS: try adding math</li>
<li>U+229F SQUARED MINUS: try adding math</li>
<li>U+22A0 SQUARED TIMES: try adding math</li>
<li>U+22A1 SQUARED DOT OPERATOR: try adding math</li>
<li>U+22A2 RIGHT TACK: try adding math</li>
<li>U+22A3 LEFT TACK: try adding math</li>
<li>U+22A4 DOWN TACK: try adding math</li>
<li>U+22A5 UP TACK: try adding math</li>
<li>U+22A6 ASSERTION: try adding math</li>
<li>U+22A7 MODELS: try adding math</li>
<li>U+22A8 TRUE: try adding math</li>
<li>U+22A9 FORCES: try adding math</li>
<li>U+22AA TRIPLE VERTICAL BAR RIGHT TURNSTILE: try adding math</li>
<li>U+22AB DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE: try adding math</li>
<li>U+22AC DOES NOT PROVE: try adding math</li>
<li>U+22AD NOT TRUE: try adding math</li>
<li>U+22AE DOES NOT FORCE: try adding math</li>
<li>U+22AF NEGATED DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE: try adding math</li>
<li>U+22B0 PRECEDES UNDER RELATION: try adding math</li>
<li>U+22B1 SUCCEEDS UNDER RELATION: try adding math</li>
<li>U+22B2 NORMAL SUBGROUP OF: try adding math</li>
<li>U+22B3 CONTAINS AS NORMAL SUBGROUP: try adding math</li>
<li>U+22B4 NORMAL SUBGROUP OF OR EQUAL TO: try adding math</li>
<li>U+22B5 CONTAINS AS NORMAL SUBGROUP OR EQUAL TO: try adding math</li>
<li>U+22B6 ORIGINAL OF: try adding math</li>
<li>U+22B7 IMAGE OF: try adding math</li>
<li>U+22B8 MULTIMAP: try adding math</li>
<li>U+22B9 HERMITIAN CONJUGATE MATRIX: try adding math</li>
<li>U+22BA INTERCALATE: try adding math</li>
<li>U+22BB XOR: try adding math</li>
<li>U+22BC NAND: try adding math</li>
<li>U+22BD NOR: try adding math</li>
<li>U+22BE RIGHT ANGLE WITH ARC: try adding math</li>
<li>U+22BF RIGHT TRIANGLE: try adding math</li>
<li>U+22C0 N-ARY LOGICAL AND: try adding math</li>
<li>U+22C1 N-ARY LOGICAL OR: try adding math</li>
<li>U+22C2 N-ARY INTERSECTION: try adding math</li>
<li>U+22C3 N-ARY UNION: try adding math</li>
<li>U+22C4 DIAMOND OPERATOR: try adding one of: symbols, math</li>
<li>U+22C5 DOT OPERATOR: try adding one of: symbols, math</li>
<li>U+22C6 STAR OPERATOR: try adding one of: symbols, math</li>
<li>U+22C7 DIVISION TIMES: try adding math</li>
<li>U+22C8 BOWTIE: try adding math</li>
<li>U+22C9 LEFT NORMAL FACTOR SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CA RIGHT NORMAL FACTOR SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CB LEFT SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CC RIGHT SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CD REVERSED TILDE EQUALS: try adding math</li>
<li>U+22CE CURLY LOGICAL OR: try adding math</li>
<li>U+22CF CURLY LOGICAL AND: try adding math</li>
<li>U+22D0 DOUBLE SUBSET: try adding math</li>
<li>U+22D1 DOUBLE SUPERSET: try adding math</li>
<li>U+22D2 DOUBLE INTERSECTION: try adding math</li>
<li>U+22D3 DOUBLE UNION: try adding math</li>
<li>U+22D4 PITCHFORK: try adding math</li>
<li>U+22D5 EQUAL AND PARALLEL TO: try adding math</li>
<li>U+22D6 LESS-THAN WITH DOT: try adding math</li>
<li>U+22D7 GREATER-THAN WITH DOT: try adding math</li>
<li>U+22D8 VERY MUCH LESS-THAN: try adding math</li>
<li>U+22D9 VERY MUCH GREATER-THAN: try adding math</li>
<li>U+22DA LESS-THAN EQUAL TO OR GREATER-THAN: try adding math</li>
<li>U+22DB GREATER-THAN EQUAL TO OR LESS-THAN: try adding math</li>
<li>U+22DC EQUAL TO OR LESS-THAN: try adding math</li>
<li>U+22DD EQUAL TO OR GREATER-THAN: try adding math</li>
<li>U+22DE EQUAL TO OR PRECEDES: try adding math</li>
<li>U+22DF EQUAL TO OR SUCCEEDS: try adding math</li>
<li>U+22E0 DOES NOT PRECEDE OR EQUAL: try adding math</li>
<li>U+22E1 DOES NOT SUCCEED OR EQUAL: try adding math</li>
<li>U+22E2 NOT SQUARE IMAGE OF OR EQUAL TO: try adding math</li>
<li>U+22E3 NOT SQUARE ORIGINAL OF OR EQUAL TO: try adding math</li>
<li>U+22E4 SQUARE IMAGE OF OR NOT EQUAL TO: try adding math</li>
<li>U+22E5 SQUARE ORIGINAL OF OR NOT EQUAL TO: try adding math</li>
<li>U+22E6 LESS-THAN BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E7 GREATER-THAN BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E8 PRECEDES BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E9 SUCCEEDS BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22EA NOT NORMAL SUBGROUP OF: try adding math</li>
<li>U+22EB DOES NOT CONTAIN AS NORMAL SUBGROUP: try adding math</li>
<li>U+22EC NOT NORMAL SUBGROUP OF OR EQUAL TO: try adding math</li>
<li>U+22ED DOES NOT CONTAIN AS NORMAL SUBGROUP OR EQUAL: try adding math</li>
<li>U+22EE VERTICAL ELLIPSIS: try adding math</li>
<li>U+22EF MIDLINE HORIZONTAL ELLIPSIS: try adding math</li>
<li>U+22F0 UP RIGHT DIAGONAL ELLIPSIS: try adding math</li>
<li>U+22F1 DOWN RIGHT DIAGONAL ELLIPSIS: try adding math</li>
<li>U+22F2 ELEMENT OF WITH LONG HORIZONTAL STROKE: try adding math</li>
<li>U+22F3 ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22F4 SMALL ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22F5 ELEMENT OF WITH DOT ABOVE: try adding math</li>
<li>U+22F6 ELEMENT OF WITH OVERBAR: try adding math</li>
<li>U+22F7 SMALL ELEMENT OF WITH OVERBAR: try adding math</li>
<li>U+22F8 ELEMENT OF WITH UNDERBAR: try adding math</li>
<li>U+22F9 ELEMENT OF WITH TWO HORIZONTAL STROKES: try adding math</li>
<li>U+22FA CONTAINS WITH LONG HORIZONTAL STROKE: try adding math</li>
<li>U+22FB CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22FC SMALL CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22FD CONTAINS WITH OVERBAR: try adding math</li>
<li>U+22FE SMALL CONTAINS WITH OVERBAR: try adding math</li>
<li>U+22FF Z NOTATION BAG MEMBERSHIP: try adding math</li>
<li>U+2460 CIRCLED DIGIT ONE: try adding one of: yi, symbols, mongolian</li>
<li>U+2461 CIRCLED DIGIT TWO: try adding one of: yi, symbols, mongolian</li>
<li>U+2462 CIRCLED DIGIT THREE: try adding one of: yi, symbols, mongolian</li>
<li>U+2463 CIRCLED DIGIT FOUR: try adding one of: yi, symbols, mongolian</li>
<li>U+2464 CIRCLED DIGIT FIVE: try adding one of: yi, symbols, mongolian</li>
<li>U+2465 CIRCLED DIGIT SIX: try adding one of: yi, symbols, mongolian</li>
<li>U+2466 CIRCLED DIGIT SEVEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2467 CIRCLED DIGIT EIGHT: try adding one of: yi, symbols, mongolian</li>
<li>U+2468 CIRCLED DIGIT NINE: try adding one of: yi, symbols, mongolian</li>
<li>U+2469 CIRCLED NUMBER TEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246A CIRCLED NUMBER ELEVEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246B CIRCLED NUMBER TWELVE: try adding one of: yi, symbols, mongolian</li>
<li>U+246C CIRCLED NUMBER THIRTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246D CIRCLED NUMBER FOURTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246E CIRCLED NUMBER FIFTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246F CIRCLED NUMBER SIXTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2470 CIRCLED NUMBER SEVENTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2471 CIRCLED NUMBER EIGHTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2472 CIRCLED NUMBER NINETEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2473 CIRCLED NUMBER TWENTY: try adding one of: yi, symbols, mongolian</li>
<li>U+2474 PARENTHESIZED DIGIT ONE: try adding one of: symbols, math</li>
<li>U+2475 PARENTHESIZED DIGIT TWO: try adding one of: symbols, math</li>
<li>U+2476 PARENTHESIZED DIGIT THREE: try adding symbols</li>
<li>U+2477 PARENTHESIZED DIGIT FOUR: try adding symbols</li>
<li>U+2478 PARENTHESIZED DIGIT FIVE: try adding symbols</li>
<li>U+2479 PARENTHESIZED DIGIT SIX: try adding symbols</li>
<li>U+247A PARENTHESIZED DIGIT SEVEN: try adding symbols</li>
<li>U+247B PARENTHESIZED DIGIT EIGHT: try adding symbols</li>
<li>U+247C PARENTHESIZED DIGIT NINE: try adding symbols</li>
<li>U+247D PARENTHESIZED NUMBER TEN: try adding symbols</li>
<li>U+247E PARENTHESIZED NUMBER ELEVEN: try adding symbols</li>
<li>U+247F PARENTHESIZED NUMBER TWELVE: try adding symbols</li>
<li>U+2480 PARENTHESIZED NUMBER THIRTEEN: try adding symbols</li>
<li>U+2481 PARENTHESIZED NUMBER FOURTEEN: try adding symbols</li>
<li>U+2482 PARENTHESIZED NUMBER FIFTEEN: try adding symbols</li>
<li>U+2483 PARENTHESIZED NUMBER SIXTEEN: try adding symbols</li>
<li>U+2484 PARENTHESIZED NUMBER SEVENTEEN: try adding symbols</li>
<li>U+2485 PARENTHESIZED NUMBER EIGHTEEN: try adding symbols</li>
<li>U+2486 PARENTHESIZED NUMBER NINETEEN: try adding symbols</li>
<li>U+2487 PARENTHESIZED NUMBER TWENTY: try adding symbols</li>
<li>U+2488 DIGIT ONE FULL STOP: try adding symbols</li>
<li>U+2489 DIGIT TWO FULL STOP: try adding symbols</li>
<li>U+248A DIGIT THREE FULL STOP: try adding symbols</li>
<li>U+248B DIGIT FOUR FULL STOP: try adding symbols</li>
<li>U+248C DIGIT FIVE FULL STOP: try adding symbols</li>
<li>U+248D DIGIT SIX FULL STOP: try adding symbols</li>
<li>U+248E DIGIT SEVEN FULL STOP: try adding symbols</li>
<li>U+248F DIGIT EIGHT FULL STOP: try adding symbols</li>
<li>U+2490 DIGIT NINE FULL STOP: try adding symbols</li>
<li>U+2491 NUMBER TEN FULL STOP: try adding symbols</li>
<li>U+2492 NUMBER ELEVEN FULL STOP: try adding symbols</li>
<li>U+2493 NUMBER TWELVE FULL STOP: try adding symbols</li>
<li>U+2494 NUMBER THIRTEEN FULL STOP: try adding symbols</li>
<li>U+2495 NUMBER FOURTEEN FULL STOP: try adding symbols</li>
<li>U+2496 NUMBER FIFTEEN FULL STOP: try adding symbols</li>
<li>U+2497 NUMBER SIXTEEN FULL STOP: try adding symbols</li>
<li>U+2498 NUMBER SEVENTEEN FULL STOP: try adding symbols</li>
<li>U+2499 NUMBER EIGHTEEN FULL STOP: try adding symbols</li>
<li>U+249A NUMBER NINETEEN FULL STOP: try adding symbols</li>
<li>U+249B NUMBER TWENTY FULL STOP: try adding symbols</li>
<li>U+249C PARENTHESIZED LATIN SMALL LETTER A: try adding symbols</li>
<li>U+249D PARENTHESIZED LATIN SMALL LETTER B: try adding symbols</li>
<li>U+249E PARENTHESIZED LATIN SMALL LETTER C: try adding symbols</li>
<li>U+249F PARENTHESIZED LATIN SMALL LETTER D: try adding symbols</li>
<li>U+24A0 PARENTHESIZED LATIN SMALL LETTER E: try adding symbols</li>
<li>U+24A1 PARENTHESIZED LATIN SMALL LETTER F: try adding symbols</li>
<li>U+24A2 PARENTHESIZED LATIN SMALL LETTER G: try adding symbols</li>
<li>U+24A3 PARENTHESIZED LATIN SMALL LETTER H: try adding symbols</li>
<li>U+24A4 PARENTHESIZED LATIN SMALL LETTER I: try adding symbols</li>
<li>U+24A5 PARENTHESIZED LATIN SMALL LETTER J: try adding symbols</li>
<li>U+24A6 PARENTHESIZED LATIN SMALL LETTER K: try adding symbols</li>
<li>U+24A7 PARENTHESIZED LATIN SMALL LETTER L: try adding symbols</li>
<li>U+24A8 PARENTHESIZED LATIN SMALL LETTER M: try adding symbols</li>
<li>U+24A9 PARENTHESIZED LATIN SMALL LETTER N: try adding symbols</li>
<li>U+24AA PARENTHESIZED LATIN SMALL LETTER O: try adding symbols</li>
<li>U+24AB PARENTHESIZED LATIN SMALL LETTER P: try adding symbols</li>
<li>U+24AC PARENTHESIZED LATIN SMALL LETTER Q: try adding symbols</li>
<li>U+24AD PARENTHESIZED LATIN SMALL LETTER R: try adding symbols</li>
<li>U+24AE PARENTHESIZED LATIN SMALL LETTER S: try adding symbols</li>
<li>U+24AF PARENTHESIZED LATIN SMALL LETTER T: try adding symbols</li>
<li>U+24B0 PARENTHESIZED LATIN SMALL LETTER U: try adding symbols</li>
<li>U+24B1 PARENTHESIZED LATIN SMALL LETTER V: try adding symbols</li>
<li>U+24B2 PARENTHESIZED LATIN SMALL LETTER W: try adding symbols</li>
<li>U+24B3 PARENTHESIZED LATIN SMALL LETTER X: try adding symbols</li>
<li>U+24B4 PARENTHESIZED LATIN SMALL LETTER Y: try adding symbols</li>
<li>U+24B5 PARENTHESIZED LATIN SMALL LETTER Z: try adding symbols</li>
<li>U+24B6 CIRCLED LATIN CAPITAL LETTER A: try adding symbols</li>
<li>U+24B7 CIRCLED LATIN CAPITAL LETTER B: try adding symbols</li>
<li>U+24B8 CIRCLED LATIN CAPITAL LETTER C: try adding symbols</li>
<li>U+24B9 CIRCLED LATIN CAPITAL LETTER D: try adding symbols</li>
<li>U+24BA CIRCLED LATIN CAPITAL LETTER E: try adding symbols</li>
<li>U+24BB CIRCLED LATIN CAPITAL LETTER F: try adding symbols</li>
<li>U+24BC CIRCLED LATIN CAPITAL LETTER G: try adding symbols</li>
<li>U+24BD CIRCLED LATIN CAPITAL LETTER H: try adding symbols</li>
<li>U+24BE CIRCLED LATIN CAPITAL LETTER I: try adding symbols</li>
<li>U+24BF CIRCLED LATIN CAPITAL LETTER J: try adding symbols</li>
<li>U+24C0 CIRCLED LATIN CAPITAL LETTER K: try adding symbols</li>
<li>U+24C1 CIRCLED LATIN CAPITAL LETTER L: try adding symbols</li>
<li>U+24C2 CIRCLED LATIN CAPITAL LETTER M: try adding symbols</li>
<li>U+24C3 CIRCLED LATIN CAPITAL LETTER N: try adding symbols</li>
<li>U+24C4 CIRCLED LATIN CAPITAL LETTER O: try adding symbols</li>
<li>U+24C5 CIRCLED LATIN CAPITAL LETTER P: try adding symbols</li>
<li>U+24C6 CIRCLED LATIN CAPITAL LETTER Q: try adding symbols</li>
<li>U+24C7 CIRCLED LATIN CAPITAL LETTER R: try adding symbols</li>
<li>U+24C8 CIRCLED LATIN CAPITAL LETTER S: try adding symbols</li>
<li>U+24C9 CIRCLED LATIN CAPITAL LETTER T: try adding symbols</li>
<li>U+24CA CIRCLED LATIN CAPITAL LETTER U: try adding symbols</li>
<li>U+24CB CIRCLED LATIN CAPITAL LETTER V: try adding symbols</li>
<li>U+24CC CIRCLED LATIN CAPITAL LETTER W: try adding symbols</li>
<li>U+24CD CIRCLED LATIN CAPITAL LETTER X: try adding symbols</li>
<li>U+24CE CIRCLED LATIN CAPITAL LETTER Y: try adding symbols</li>
<li>U+24CF CIRCLED LATIN CAPITAL LETTER Z: try adding symbols</li>
<li>U+24D0 CIRCLED LATIN SMALL LETTER A: try adding symbols</li>
<li>U+24D1 CIRCLED LATIN SMALL LETTER B: try adding symbols</li>
<li>U+24D2 CIRCLED LATIN SMALL LETTER C: try adding symbols</li>
<li>U+24D3 CIRCLED LATIN SMALL LETTER D: try adding symbols</li>
<li>U+24D4 CIRCLED LATIN SMALL LETTER E: try adding symbols</li>
<li>U+24D5 CIRCLED LATIN SMALL LETTER F: try adding symbols</li>
<li>U+24D6 CIRCLED LATIN SMALL LETTER G: try adding symbols</li>
<li>U+24D7 CIRCLED LATIN SMALL LETTER H: try adding symbols</li>
<li>U+24D8 CIRCLED LATIN SMALL LETTER I: try adding symbols</li>
<li>U+24D9 CIRCLED LATIN SMALL LETTER J: try adding symbols</li>
<li>U+24DA CIRCLED LATIN SMALL LETTER K: try adding symbols</li>
<li>U+24DB CIRCLED LATIN SMALL LETTER L: try adding symbols</li>
<li>U+24DC CIRCLED LATIN SMALL LETTER M: try adding symbols</li>
<li>U+24DD CIRCLED LATIN SMALL LETTER N: try adding symbols</li>
<li>U+24DE CIRCLED LATIN SMALL LETTER O: try adding symbols</li>
<li>U+24DF CIRCLED LATIN SMALL LETTER P: try adding symbols</li>
<li>U+24E0 CIRCLED LATIN SMALL LETTER Q: try adding symbols</li>
<li>U+24E1 CIRCLED LATIN SMALL LETTER R: try adding symbols</li>
<li>U+24E2 CIRCLED LATIN SMALL LETTER S: try adding symbols</li>
<li>U+24E3 CIRCLED LATIN SMALL LETTER T: try adding symbols</li>
<li>U+24E4 CIRCLED LATIN SMALL LETTER U: try adding symbols</li>
<li>U+24E5 CIRCLED LATIN SMALL LETTER V: try adding symbols</li>
<li>U+24E6 CIRCLED LATIN SMALL LETTER W: try adding symbols</li>
<li>U+24E7 CIRCLED LATIN SMALL LETTER X: try adding symbols</li>
<li>U+24E8 CIRCLED LATIN SMALL LETTER Y: try adding symbols</li>
<li>U+24E9 CIRCLED LATIN SMALL LETTER Z: try adding symbols</li>
<li>U+24EA CIRCLED DIGIT ZERO: try adding symbols</li>
<li>U+24EB NEGATIVE CIRCLED NUMBER ELEVEN: try adding symbols</li>
<li>U+24EC NEGATIVE CIRCLED NUMBER TWELVE: try adding symbols</li>
<li>U+24ED NEGATIVE CIRCLED NUMBER THIRTEEN: try adding symbols</li>
<li>U+24EE NEGATIVE CIRCLED NUMBER FOURTEEN: try adding symbols</li>
<li>U+24EF NEGATIVE CIRCLED NUMBER FIFTEEN: try adding symbols</li>
<li>U+24F0 NEGATIVE CIRCLED NUMBER SIXTEEN: try adding symbols</li>
<li>U+24F1 NEGATIVE CIRCLED NUMBER SEVENTEEN: try adding symbols</li>
<li>U+24F2 NEGATIVE CIRCLED NUMBER EIGHTEEN: try adding symbols</li>
<li>U+24F3 NEGATIVE CIRCLED NUMBER NINETEEN: try adding symbols</li>
<li>U+24F4 NEGATIVE CIRCLED NUMBER TWENTY: try adding symbols</li>
<li>U+24F5 DOUBLE CIRCLED DIGIT ONE: try adding symbols</li>
<li>U+24F6 DOUBLE CIRCLED DIGIT TWO: try adding symbols</li>
<li>U+24F7 DOUBLE CIRCLED DIGIT THREE: try adding symbols</li>
<li>U+24F8 DOUBLE CIRCLED DIGIT FOUR: try adding symbols</li>
<li>U+24F9 DOUBLE CIRCLED DIGIT FIVE: try adding symbols</li>
<li>U+24FA DOUBLE CIRCLED DIGIT SIX: try adding symbols</li>
<li>U+24FB DOUBLE CIRCLED DIGIT SEVEN: try adding symbols</li>
<li>U+24FC DOUBLE CIRCLED DIGIT EIGHT: try adding symbols</li>
<li>U+24FD DOUBLE CIRCLED DIGIT NINE: try adding symbols</li>
<li>U+24FE DOUBLE CIRCLED NUMBER TEN: try adding symbols</li>
<li>U+24FF NEGATIVE CIRCLED DIGIT ZERO: try adding symbols</li>
<li>U+25CC DOTTED CIRCLE: try adding one of: syriac, armenian, tai-le, tamil, zanabazar-square, coptic, mende-kikakui, khudawadi, gujarati, kayah-li, music, mandaic, elbasan, manichaean, soyombo, tagbanwa, thaana, hanunoo, khojki, devanagari, tifinagh, meetei-mayek, pahawh-hmong, sharada, oriya, newa, kharoshthi, buhid, phags-pa, bassa-vah, balinese, canadian-aboriginal, kannada, symbols, psalter-pahlavi, bhaiksuki, rejang, old-permic, syloti-nagri, warang-citi, kaithi, siddham, sogdian, khmer, saurashtra, ahom, batak, new-tai-lue, dogra, math, sundanese, mongolian, lepcha, nko, tibetan, buginese, sinhala, caucasian-albanian, myanmar, malayalam, osage, tirhuta, lao, javanese, thai, chakma, mahajani, modi, masaram-gondi, brahmi, hanifi-rohingya, duployan, takri, miao, limbu, tagalog, tai-viet, telugu, yi, gurmukhi, wancho, marchen, hebrew, grantha, gunjala-gondi, bengali, adlam, cham, tai-tham</li>
<li>U+25CF BLACK CIRCLE: try adding symbols</li>
<li>U+25EF LARGE CIRCLE: try adding symbols</li>
<li>U+2776 DINGBAT NEGATIVE CIRCLED DIGIT ONE: try adding symbols</li>
<li>U+2777 DINGBAT NEGATIVE CIRCLED DIGIT TWO: try adding symbols</li>
<li>U+2778 DINGBAT NEGATIVE CIRCLED DIGIT THREE: try adding symbols</li>
<li>U+2779 DINGBAT NEGATIVE CIRCLED DIGIT FOUR: try adding symbols</li>
<li>U+277A DINGBAT NEGATIVE CIRCLED DIGIT FIVE: try adding symbols</li>
<li>U+277B DINGBAT NEGATIVE CIRCLED DIGIT SIX: try adding symbols</li>
<li>U+277C DINGBAT NEGATIVE CIRCLED DIGIT SEVEN: try adding symbols</li>
<li>U+277D DINGBAT NEGATIVE CIRCLED DIGIT EIGHT: try adding symbols</li>
<li>U+277E DINGBAT NEGATIVE CIRCLED DIGIT NINE: try adding symbols</li>
<li>U+277F DINGBAT NEGATIVE CIRCLED NUMBER TEN: try adding symbols</li>
<li>U+27E8 MATHEMATICAL LEFT ANGLE BRACKET: try adding math</li>
<li>U+27E9 MATHEMATICAL RIGHT ANGLE BRACKET: try adding math</li>
<li>U+27EA MATHEMATICAL LEFT DOUBLE ANGLE BRACKET: try adding math</li>
<li>U+27EB MATHEMATICAL RIGHT DOUBLE ANGLE BRACKET: try adding math</li>
<li>U+27F2 ANTICLOCKWISE GAPPED CIRCLE ARROW: try adding math</li>
<li>U+27F3 CLOCKWISE GAPPED CIRCLE ARROW: try adding math</li>
<li>U+27F4 RIGHT ARROW WITH CIRCLED PLUS: try adding math</li>
<li>U+27F5 LONG LEFTWARDS ARROW: try adding math</li>
<li>U+27F6 LONG RIGHTWARDS ARROW: try adding math</li>
<li>U+27F7 LONG LEFT RIGHT ARROW: try adding math</li>
<li>U+27F8 LONG LEFTWARDS DOUBLE ARROW: try adding math</li>
<li>U+27F9 LONG RIGHTWARDS DOUBLE ARROW: try adding math</li>
<li>U+27FA LONG LEFT RIGHT DOUBLE ARROW: try adding math</li>
<li>U+27FB LONG LEFTWARDS ARROW FROM BAR: try adding math</li>
<li>U+27FC LONG RIGHTWARDS ARROW FROM BAR: try adding math</li>
<li>U+27FD LONG LEFTWARDS DOUBLE ARROW FROM BAR: try adding math</li>
<li>U+27FE LONG RIGHTWARDS DOUBLE ARROW FROM BAR: try adding math</li>
<li>U+27FF LONG RIGHTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+2E17 DOUBLE OBLIQUE HYPHEN: try adding coptic</li>
</ul>
<p>Or you can add the above codepoints to one of the subsets supported by the font: <code>cyrillic</code>, <code>cyrillic-ext</code>, <code>greek</code>, <code>greek-ext</code>, <code>latin</code>, <code>latin-ext</code>, <code>vietnamese</code></p>
 [code: unreachable-subsetting]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#outline-alignment-miss">outline_alignment_miss</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have on-curve points which have potentially incorrect y coordinates:</p>
<pre><code>* uni0306_hookabovecomb.case: X=706.0,Y=1479.0 (should be at cap-height 1480?)

* uni1EAA (U+1EAA): X=551.0,Y=2046.0 (should be at ascender 2048?)

* uni1EC4 (U+1EC4): X=477.0,Y=2046.0 (should be at ascender 2048?)

* uni1ED6 (U+1ED6): X=674.0,Y=2046.0 (should be at ascender 2048?)

* uni2147 (U+2147): X=761.0,Y=1.0 (should be at baseline 0?)

* zero.zero.subscript: X=262.0,Y=1.0 (should be at baseline 0?)

* zero.zero.subscript.pnum: X=247.0,Y=1.0 (should be at baseline 0?)

* zero.zero.subscript.tnum: X=480.0,Y=1.0 (should be at baseline 0?)

* zero.zero.superior: X=534.0,Y=1479.0 (should be at cap-height 1480?)

* zero.zero.superior.pnum: X=519.0,Y=1479.0 (should be at cap-height 1480?)

* zero.zero.superior.tnum: X=752.0,Y=1479.0 (should be at cap-height 1480?)
</code></pre>
 [code: found-misalignments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#outline-jaggy-segments">outline_jaggy_segments</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have jaggy segments:</p>
<pre><code>* uni210A (U+210A): B&lt;&lt;379.0,397.0&gt;-&lt;397.0,417.0&gt;-&lt;418.0,440.0&gt;-&lt;441.0,468.0&gt;&gt;/B&lt;&lt;441.0,468.0&gt;-&lt;379.0,380.0&gt;-&lt;348.0,299.0&gt;-&lt;348.0,224.0&gt;&gt; = 4.23422462768641

* uni210A (U+210A): B&lt;&lt;733.0,59.0&gt;-&lt;758.0,80.0&gt;-&lt;776.0,98.0&gt;-&lt;787.0,110.0&gt;&gt;/L&lt;&lt;787.0,110.0&gt;--&lt;717.0,-11.0&gt;&gt; = 12.460533457013435

* uni210B (U+210B): B&lt;&lt;1077.0,1099.0&gt;-&lt;1118.0,1132.0&gt;-&lt;1155.0,1165.0&gt;-&lt;1188.0,1195.0&gt;&gt;/B&lt;&lt;1188.0,1195.0&gt;-&lt;1101.0,1089.0&gt;-&lt;1030.0,986.0&gt;-&lt;975.0,888.0&gt;&gt; = 8.34871162099596

* uni2133 (U+2133): B&lt;&lt;2219.0,1344.0&gt;-&lt;2278.0,1392.0&gt;-&lt;2318.0,1423.0&gt;-&lt;2340.0,1438.0&gt;&gt;/B&lt;&lt;2340.0,1438.0&gt;-&lt;2332.0,1430.0&gt;-&lt;2315.0,1412.0&gt;-&lt;2291.0,1384.0&gt;&gt; = 10.713123022791033
</code></pre>
 [code: found-jaggy-segments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 achVendID. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-vendor-id">googlefonts/vendor_id</a></summary>
    <div>







* ⚠️ **WARN** <p>OS/2 VendorID is 'PfEd', a font editor default. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at <a href="https://www.microsoft.com/typography/links/vendorlist.aspx">https://www.microsoft.com/typography/links/vendorlist.aspx</a></p>
 [code: bad]



</div>
</details>
</div>
</details>

<details><summary>[9] GiphursExtraBlack-Regular.otf</summary>
<div>
<details>
    <summary>💥 <b>ERROR</b> Shapes languages in all GF glyphsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-glyphsets-shape-languages">googlefonts/glyphsets/shape_languages</a></summary>
    <div>







* 💥 **ERROR** <p>Failed with TypeError: argument 'lang': 'NoneType' object cannot be converted to 'Language'</p>
<pre><code>  File &quot;/media/corne2plum3/Users/corne/Fonts/- My Fonts/Giphurs/venv/lib/python3.12/site-packages/fontbakery/checkrunner.py&quot;, line 222, in _run_check
    subresults = list(subresults)
                 ^^^^^^^^^^^^^^^^
  File &quot;/media/corne2plum3/Users/corne/Fonts/- My Fonts/Giphurs/venv/lib/python3.12/site-packages/fontbakery/checks/vendorspecific/googlefonts/glyphsets/shape_languages.py&quot;, line 49, in check_glyphsets_shape_languages
    reporter = shaperglot_checker.check(shaperglot_languages[language_code])
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

</code></pre>
 [code: failed-check]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check GDEF mark glyph class doesn't have characters that are not marks. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.html#opentype-gdef-non-mark-chars">opentype/gdef_non_mark_chars</a></summary>
    <div>







* ⚠️ **WARN** <p>The following non-mark characters should not be in the GDEF mark glyph class:
U+0384, U+0385, U+1FBD, U+1FBE, U+1FBF, U+1FC0, U+1FC1, U+1FCD, U+1FCE, U+1FCF, U+1FDD, U+1FDE, U+1FDF, U+1FED, U+1FEE, U+1FEF, U+1FFD and U+1FFE</p>
 [code: non-mark-chars]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check glyphs in mark glyph class are non-spacing. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/opentype.html#opentype-gdef-spacing-marks">opentype/gdef_spacing_marks</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs seem to be spacing (because they have width &gt; 0 on the hmtx table) so they may be in the GDEF mark glyph class by mistake, or they should have zero width instead:
dieresistonos (U+0385), tonos (U+0384), tonos2 (unencoded), uni1FBD (U+1FBD), uni1FBE (U+1FBE), uni1FBF (U+1FBF), uni1FC0 (U+1FC0), uni1FC1 (U+1FC1), uni1FCD (U+1FCD), uni1FCE (U+1FCE), uni1FCF (U+1FCF), uni1FDD (U+1FDD), uni1FDE (U+1FDE), uni1FDF (U+1FDF), uni1FED (U+1FED), uni1FEE (U+1FEE), uni1FEF (U+1FEF), uni1FFD (U+1FFD) and uni1FFE (U+1FFE)</p>
 [code: spacing-mark-glyphs]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check font contains no unreachable glyphs <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#unreachable-glyphs">unreachable_glyphs</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs could not be reached by codepoint or substitution rules:</p>
<pre><code>- acutecomb.case

- acutecomb_uni0307

- double_circle_empty

- gravecomb.case

- tildecomb.case

- tildecomb_uni0308.case

- tonos2

- uni0302.case

- uni0304.case

- uni0306.case

- uni0306_acutecomb.case

- uni0306_gravecomb.case

- uni0306_hookabovecomb.case

- uni0307.case

- uni0308.case

- uni030B.case

- uni030C.case

- uni030C_uni0307.case

- uni030F.case
</code></pre>
 [code: unreachable-glyphs]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Validate size, and resolution of article images, and ensure article page has minimum length and includes visual assets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-article-images">googlefonts/article/images</a></summary>
    <div>







* ⚠️ **WARN** <p>Family metadata at fonts/otf does not have an article.</p>
 [code: lacks-article]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Check for codepoints not covered by METADATA subsets. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-metadata-unreachable-subsetting">googlefonts/metadata/unreachable_subsetting</a></summary>
    <div>







* ⚠️ **WARN** <p>The following codepoints supported by the font are not covered by
any subsets defined in the font's metadata file, and will never
be served. You can solve this by either manually adding additional
subset declarations to METADATA.pb, or by editing the glyphset
definitions.</p>
<ul>
<li>U+02CD MODIFIER LETTER LOW MACRON: try adding lisu</li>
<li>U+02D8 BREVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02D9 DOT ABOVE: try adding one of: canadian-aboriginal, yi</li>
<li>U+02DB OGONEK: try adding one of: canadian-aboriginal, yi</li>
<li>U+0302 COMBINING CIRCUMFLEX ACCENT: try adding one of: tifinagh, coptic, math, cherokee</li>
<li>U+0306 COMBINING BREVE: try adding one of: old-permic, tifinagh</li>
<li>U+0307 COMBINING DOT ABOVE: try adding one of: old-permic, syriac, tifinagh, coptic, malayalam, math, tai-le, todhri, canadian-aboriginal, hebrew, duployan</li>
<li>U+030A COMBINING RING ABOVE: try adding one of: syriac, duployan</li>
<li>U+030B COMBINING DOUBLE ACUTE ACCENT: try adding one of: cherokee, osage</li>
<li>U+030C COMBINING CARON: try adding one of: tai-le, cherokee</li>
<li>U+030D COMBINING VERTICAL LINE ABOVE: try adding sunuwar</li>
<li>U+030F COMBINING DOUBLE GRAVE ACCENT: not included in any glyphset definition</li>
<li>U+0311 COMBINING INVERTED BREVE: try adding one of: coptic, todhri</li>
<li>U+0312 COMBINING TURNED COMMA ABOVE: try adding math</li>
<li>U+0313 COMBINING COMMA ABOVE: try adding one of: old-permic, todhri</li>
<li>U+0314 COMBINING REVERSED COMMA ABOVE: not included in any glyphset definition</li>
<li>U+0315 COMBINING COMMA ABOVE RIGHT: try adding math</li>
<li>U+031B COMBINING HORN: not included in any glyphset definition</li>
<li>U+0324 COMBINING DIAERESIS BELOW: try adding one of: syriac, duployan, cherokee</li>
<li>U+0325 COMBINING RING BELOW: try adding syriac</li>
<li>U+0326 COMBINING COMMA BELOW: try adding math</li>
<li>U+0327 COMBINING CEDILLA: try adding math</li>
<li>U+0328 COMBINING OGONEK: not included in any glyphset definition</li>
<li>U+032D COMBINING CIRCUMFLEX ACCENT BELOW: try adding one of: syriac, sunuwar</li>
<li>U+032E COMBINING BREVE BELOW: try adding syriac</li>
<li>U+032F COMBINING INVERTED BREVE BELOW: try adding math</li>
<li>U+0330 COMBINING TILDE BELOW: try adding one of: syriac, math, cherokee</li>
<li>U+0331 COMBINING MACRON BELOW: try adding one of: thai, syriac, gothic, sunuwar, tifinagh, cherokee, caucasian-albanian</li>
<li>U+0337 COMBINING SHORT SOLIDUS OVERLAY: not included in any glyphset definition</li>
<li>U+0338 COMBINING LONG SOLIDUS OVERLAY: try adding math</li>
<li>U+0340 COMBINING GRAVE TONE MARK: not included in any glyphset definition</li>
<li>U+0341 COMBINING ACUTE TONE MARK: not included in any glyphset definition</li>
<li>U+0342 COMBINING GREEK PERISPOMENI: not included in any glyphset definition</li>
<li>U+0343 COMBINING GREEK KORONIS: not included in any glyphset definition</li>
<li>U+0345 COMBINING GREEK YPOGEGRAMMENI: not included in any glyphset definition</li>
<li>U+0357 COMBINING RIGHT HALF RING ABOVE: not included in any glyphset definition</li>
<li>U+035F COMBINING DOUBLE MACRON BELOW: not included in any glyphset definition</li>
<li>U+1DC4 COMBINING MACRON-ACUTE: not included in any glyphset definition</li>
<li>U+1DC5 COMBINING GRAVE-MACRON: not included in any glyphset definition</li>
<li>U+1DC6 COMBINING MACRON-GRAVE: not included in any glyphset definition</li>
<li>U+1DC7 COMBINING ACUTE-MACRON: not included in any glyphset definition</li>
<li>U+2010 HYPHEN: try adding one of: kharoshthi, syloti-nagri, lisu, kaithi, armenian, coptic, sundanese, cham, sora-sompeng, arabic, hebrew, yi, kayah-li</li>
<li>U+2011 NON-BREAKING HYPHEN: try adding one of: arabic, syloti-nagri, yi</li>
<li>U+2012 FIGURE DASH: not included in any glyphset definition</li>
<li>U+2015 HORIZONTAL BAR: try adding adlam</li>
<li>U+2016 DOUBLE VERTICAL LINE: try adding math</li>
<li>U+2017 DOUBLE LOW LINE: try adding math</li>
<li>U+201B SINGLE HIGH-REVERSED-9 QUOTATION MARK: try adding adlam</li>
<li>U+201F DOUBLE HIGH-REVERSED-9 QUOTATION MARK: not included in any glyphset definition</li>
<li>U+2021 DOUBLE DAGGER: try adding adlam</li>
<li>U+2023 TRIANGULAR BULLET: not included in any glyphset definition</li>
<li>U+2024 ONE DOT LEADER: try adding armenian</li>
<li>U+2025 TWO DOT LEADER: try adding phags-pa</li>
<li>U+2027 HYPHENATION POINT: not included in any glyphset definition</li>
<li>U+2030 PER MILLE SIGN: try adding adlam</li>
<li>U+2031 PER TEN THOUSAND SIGN: not included in any glyphset definition</li>
<li>U+2034 TRIPLE PRIME: try adding math</li>
<li>U+2035 REVERSED PRIME: try adding math</li>
<li>U+2036 REVERSED DOUBLE PRIME: try adding math</li>
<li>U+2037 REVERSED TRIPLE PRIME: try adding math</li>
<li>U+2038 CARET: try adding math</li>
<li>U+203B REFERENCE MARK: not included in any glyphset definition</li>
<li>U+203C DOUBLE EXCLAMATION MARK: try adding math</li>
<li>U+203D INTERROBANG: not included in any glyphset definition</li>
<li>U+203E OVERLINE: not included in any glyphset definition</li>
<li>U+203F UNDERTIE: not included in any glyphset definition</li>
<li>U+2040 CHARACTER TIE: try adding math</li>
<li>U+2041 CARET INSERTION POINT: not included in any glyphset definition</li>
<li>U+2042 ASTERISM: not included in any glyphset definition</li>
<li>U+2043 HYPHEN BULLET: try adding math</li>
<li>U+2045 LEFT SQUARE BRACKET WITH QUILL: not included in any glyphset definition</li>
<li>U+2046 RIGHT SQUARE BRACKET WITH QUILL: not included in any glyphset definition</li>
<li>U+2047 DOUBLE QUESTION MARK: try adding math</li>
<li>U+2048 QUESTION EXCLAMATION MARK: try adding mongolian</li>
<li>U+2049 EXCLAMATION QUESTION MARK: try adding mongolian</li>
<li>U+204A TIRONIAN SIGN ET: not included in any glyphset definition</li>
<li>U+204B REVERSED PILCROW SIGN: not included in any glyphset definition</li>
<li>U+204C BLACK LEFTWARDS BULLET: not included in any glyphset definition</li>
<li>U+204D BLACK RIGHTWARDS BULLET: not included in any glyphset definition</li>
<li>U+204E LOW ASTERISK: not included in any glyphset definition</li>
<li>U+204F REVERSED SEMICOLON: try adding one of: arabic, adlam</li>
<li>U+2050 CLOSE UP: try adding math</li>
<li>U+2051 TWO ASTERISKS ALIGNED VERTICALLY: not included in any glyphset definition</li>
<li>U+2052 COMMERCIAL MINUS SIGN: not included in any glyphset definition</li>
<li>U+2053 SWUNG DASH: try adding coptic</li>
<li>U+2054 INVERTED UNDERTIE: not included in any glyphset definition</li>
<li>U+2055 FLOWER PUNCTUATION MARK: try adding syloti-nagri</li>
<li>U+2056 THREE DOT PUNCTUATION: try adding coptic</li>
<li>U+2057 QUADRUPLE PRIME: try adding math</li>
<li>U+2058 FOUR DOT PUNCTUATION: try adding coptic</li>
<li>U+2059 FIVE DOT PUNCTUATION: try adding coptic</li>
<li>U+205A TWO DOT PUNCTUATION: try adding one of: old-turkic, carian, georgian, glagolitic, lycian, old-hungarian</li>
<li>U+205B FOUR DOT MARK: not included in any glyphset definition</li>
<li>U+205C DOTTED CROSS: not included in any glyphset definition</li>
<li>U+205D TRICOLON: try adding one of: carian, meroitic-hieroglyphs, old-hungarian, meroitic</li>
<li>U+205E VERTICAL FOUR DOTS: try adding old-hungarian</li>
<li>U+2070 SUPERSCRIPT ZERO: try adding math</li>
<li>U+2071 SUPERSCRIPT LATIN SMALL LETTER I: try adding math</li>
<li>U+2074 SUPERSCRIPT FOUR: try adding math</li>
<li>U+2075 SUPERSCRIPT FIVE: try adding math</li>
<li>U+2076 SUPERSCRIPT SIX: try adding math</li>
<li>U+2077 SUPERSCRIPT SEVEN: try adding math</li>
<li>U+2078 SUPERSCRIPT EIGHT: try adding math</li>
<li>U+2079 SUPERSCRIPT NINE: try adding math</li>
<li>U+207A SUPERSCRIPT PLUS SIGN: try adding math</li>
<li>U+207B SUPERSCRIPT MINUS: try adding math</li>
<li>U+207C SUPERSCRIPT EQUALS SIGN: try adding math</li>
<li>U+207D SUPERSCRIPT LEFT PARENTHESIS: try adding math</li>
<li>U+207E SUPERSCRIPT RIGHT PARENTHESIS: try adding math</li>
<li>U+207F SUPERSCRIPT LATIN SMALL LETTER N: try adding math</li>
<li>U+2080 SUBSCRIPT ZERO: try adding math</li>
<li>U+2081 SUBSCRIPT ONE: try adding math</li>
<li>U+2082 SUBSCRIPT TWO: try adding math</li>
<li>U+2083 SUBSCRIPT THREE: try adding math</li>
<li>U+2084 SUBSCRIPT FOUR: try adding math</li>
<li>U+2085 SUBSCRIPT FIVE: try adding math</li>
<li>U+2086 SUBSCRIPT SIX: try adding math</li>
<li>U+2087 SUBSCRIPT SEVEN: try adding math</li>
<li>U+2088 SUBSCRIPT EIGHT: try adding math</li>
<li>U+2089 SUBSCRIPT NINE: try adding math</li>
<li>U+208A SUBSCRIPT PLUS SIGN: try adding math</li>
<li>U+208B SUBSCRIPT MINUS: try adding math</li>
<li>U+208C SUBSCRIPT EQUALS SIGN: try adding math</li>
<li>U+208D SUBSCRIPT LEFT PARENTHESIS: try adding math</li>
<li>U+208E SUBSCRIPT RIGHT PARENTHESIS: try adding math</li>
<li>U+2090 LATIN SUBSCRIPT SMALL LETTER A: try adding math</li>
<li>U+2091 LATIN SUBSCRIPT SMALL LETTER E: try adding math</li>
<li>U+2092 LATIN SUBSCRIPT SMALL LETTER O: try adding math</li>
<li>U+2093 LATIN SUBSCRIPT SMALL LETTER X: try adding math</li>
<li>U+2094 LATIN SUBSCRIPT SMALL LETTER SCHWA: try adding math</li>
<li>U+2095 LATIN SUBSCRIPT SMALL LETTER H: try adding math</li>
<li>U+2096 LATIN SUBSCRIPT SMALL LETTER K: try adding math</li>
<li>U+2097 LATIN SUBSCRIPT SMALL LETTER L: try adding math</li>
<li>U+2098 LATIN SUBSCRIPT SMALL LETTER M: try adding math</li>
<li>U+2099 LATIN SUBSCRIPT SMALL LETTER N: try adding math</li>
<li>U+209A LATIN SUBSCRIPT SMALL LETTER P: try adding math</li>
<li>U+209B LATIN SUBSCRIPT SMALL LETTER S: try adding math</li>
<li>U+209C LATIN SUBSCRIPT SMALL LETTER T: try adding math</li>
<li>U+2100 ACCOUNT OF: try adding math</li>
<li>U+2101 ADDRESSED TO THE SUBJECT: try adding math</li>
<li>U+2102 DOUBLE-STRUCK CAPITAL C: try adding math</li>
<li>U+2103 DEGREE CELSIUS: try adding math</li>
<li>U+2104 CENTRE LINE SYMBOL: try adding math</li>
<li>U+2105 CARE OF: try adding math</li>
<li>U+2106 CADA UNA: try adding math</li>
<li>U+2107 EULER CONSTANT: try adding math</li>
<li>U+2108 SCRUPLE: try adding math</li>
<li>U+2109 DEGREE FAHRENHEIT: try adding math</li>
<li>U+210A SCRIPT SMALL G: try adding math</li>
<li>U+210B SCRIPT CAPITAL H: try adding math</li>
<li>U+210C BLACK-LETTER CAPITAL H: try adding math</li>
<li>U+210D DOUBLE-STRUCK CAPITAL H: try adding math</li>
<li>U+210E PLANCK CONSTANT: try adding math</li>
<li>U+210F PLANCK CONSTANT OVER TWO PI: try adding math</li>
<li>U+2110 SCRIPT CAPITAL I: try adding math</li>
<li>U+2111 BLACK-LETTER CAPITAL I: try adding math</li>
<li>U+2112 SCRIPT CAPITAL L: try adding math</li>
<li>U+2114 L B BAR SYMBOL: try adding math</li>
<li>U+2115 DOUBLE-STRUCK CAPITAL N: try adding math</li>
<li>U+2117 SOUND RECORDING COPYRIGHT: try adding math</li>
<li>U+2118 SCRIPT CAPITAL P: try adding math</li>
<li>U+2119 DOUBLE-STRUCK CAPITAL P: try adding math</li>
<li>U+211A DOUBLE-STRUCK CAPITAL Q: try adding math</li>
<li>U+211B SCRIPT CAPITAL R: try adding math</li>
<li>U+211C BLACK-LETTER CAPITAL R: try adding math</li>
<li>U+211D DOUBLE-STRUCK CAPITAL R: try adding math</li>
<li>U+211E PRESCRIPTION TAKE: try adding math</li>
<li>U+211F RESPONSE: try adding math</li>
<li>U+2120 SERVICE MARK: try adding math</li>
<li>U+2121 TELEPHONE SIGN: try adding math</li>
<li>U+2123 VERSICLE: try adding math</li>
<li>U+2124 DOUBLE-STRUCK CAPITAL Z: try adding math</li>
<li>U+2125 OUNCE SIGN: try adding math</li>
<li>U+2126 OHM SIGN: try adding math</li>
<li>U+2127 INVERTED OHM SIGN: try adding math</li>
<li>U+2128 BLACK-LETTER CAPITAL Z: try adding math</li>
<li>U+2129 TURNED GREEK SMALL LETTER IOTA: try adding math</li>
<li>U+212A KELVIN SIGN: try adding math</li>
<li>U+212B ANGSTROM SIGN: try adding math</li>
<li>U+212C SCRIPT CAPITAL B: try adding math</li>
<li>U+212D BLACK-LETTER CAPITAL C: try adding math</li>
<li>U+212E ESTIMATED SYMBOL: try adding math</li>
<li>U+212F SCRIPT SMALL E: try adding math</li>
<li>U+2130 SCRIPT CAPITAL E: try adding math</li>
<li>U+2131 SCRIPT CAPITAL F: try adding math</li>
<li>U+2132 TURNED CAPITAL F: try adding math</li>
<li>U+2133 SCRIPT CAPITAL M: try adding math</li>
<li>U+2134 SCRIPT SMALL O: try adding math</li>
<li>U+2135 ALEF SYMBOL: try adding math</li>
<li>U+2136 BET SYMBOL: try adding math</li>
<li>U+2137 GIMEL SYMBOL: try adding math</li>
<li>U+2138 DALET SYMBOL: try adding math</li>
<li>U+2139 INFORMATION SOURCE: try adding math</li>
<li>U+213A ROTATED CAPITAL Q: try adding math</li>
<li>U+213B FACSIMILE SIGN: try adding math</li>
<li>U+213C DOUBLE-STRUCK SMALL PI: try adding math</li>
<li>U+213D DOUBLE-STRUCK SMALL GAMMA: try adding math</li>
<li>U+213E DOUBLE-STRUCK CAPITAL GAMMA: try adding math</li>
<li>U+213F DOUBLE-STRUCK CAPITAL PI: try adding math</li>
<li>U+2140 DOUBLE-STRUCK N-ARY SUMMATION: try adding math</li>
<li>U+2141 TURNED SANS-SERIF CAPITAL G: try adding math</li>
<li>U+2142 TURNED SANS-SERIF CAPITAL L: try adding math</li>
<li>U+2143 REVERSED SANS-SERIF CAPITAL L: try adding math</li>
<li>U+2144 TURNED SANS-SERIF CAPITAL Y: try adding math</li>
<li>U+2145 DOUBLE-STRUCK ITALIC CAPITAL D: try adding math</li>
<li>U+2146 DOUBLE-STRUCK ITALIC SMALL D: try adding math</li>
<li>U+2147 DOUBLE-STRUCK ITALIC SMALL E: try adding math</li>
<li>U+2148 DOUBLE-STRUCK ITALIC SMALL I: try adding math</li>
<li>U+2149 DOUBLE-STRUCK ITALIC SMALL J: try adding math</li>
<li>U+214A PROPERTY LINE: try adding math</li>
<li>U+214B TURNED AMPERSAND: try adding math</li>
<li>U+214C PER SIGN: try adding math</li>
<li>U+214D AKTIESELSKAB: try adding math</li>
<li>U+214E TURNED SMALL F: try adding math</li>
<li>U+214F SYMBOL FOR SAMARITAN SOURCE: try adding math</li>
<li>U+2150 VULGAR FRACTION ONE SEVENTH: try adding symbols</li>
<li>U+2151 VULGAR FRACTION ONE NINTH: try adding symbols</li>
<li>U+2152 VULGAR FRACTION ONE TENTH: try adding symbols</li>
<li>U+2153 VULGAR FRACTION ONE THIRD: try adding symbols</li>
<li>U+2154 VULGAR FRACTION TWO THIRDS: try adding symbols</li>
<li>U+2155 VULGAR FRACTION ONE FIFTH: try adding symbols</li>
<li>U+2156 VULGAR FRACTION TWO FIFTHS: try adding symbols</li>
<li>U+2157 VULGAR FRACTION THREE FIFTHS: try adding symbols</li>
<li>U+2158 VULGAR FRACTION FOUR FIFTHS: try adding symbols</li>
<li>U+2159 VULGAR FRACTION ONE SIXTH: try adding symbols</li>
<li>U+215A VULGAR FRACTION FIVE SIXTHS: try adding symbols</li>
<li>U+215B VULGAR FRACTION ONE EIGHTH: try adding symbols</li>
<li>U+215C VULGAR FRACTION THREE EIGHTHS: try adding symbols</li>
<li>U+215D VULGAR FRACTION FIVE EIGHTHS: try adding symbols</li>
<li>U+215E VULGAR FRACTION SEVEN EIGHTHS: try adding symbols</li>
<li>U+215F FRACTION NUMERATOR ONE: try adding symbols</li>
<li>U+2160 ROMAN NUMERAL ONE: try adding symbols</li>
<li>U+2161 ROMAN NUMERAL TWO: try adding symbols</li>
<li>U+2162 ROMAN NUMERAL THREE: try adding symbols</li>
<li>U+2163 ROMAN NUMERAL FOUR: try adding symbols</li>
<li>U+2164 ROMAN NUMERAL FIVE: try adding symbols</li>
<li>U+2165 ROMAN NUMERAL SIX: try adding symbols</li>
<li>U+2166 ROMAN NUMERAL SEVEN: try adding symbols</li>
<li>U+2167 ROMAN NUMERAL EIGHT: try adding symbols</li>
<li>U+2168 ROMAN NUMERAL NINE: try adding symbols</li>
<li>U+2169 ROMAN NUMERAL TEN: try adding symbols</li>
<li>U+216A ROMAN NUMERAL ELEVEN: try adding symbols</li>
<li>U+216B ROMAN NUMERAL TWELVE: try adding symbols</li>
<li>U+216C ROMAN NUMERAL FIFTY: try adding symbols</li>
<li>U+216D ROMAN NUMERAL ONE HUNDRED: try adding symbols</li>
<li>U+216E ROMAN NUMERAL FIVE HUNDRED: try adding symbols</li>
<li>U+216F ROMAN NUMERAL ONE THOUSAND: try adding symbols</li>
<li>U+2170 SMALL ROMAN NUMERAL ONE: try adding symbols</li>
<li>U+2171 SMALL ROMAN NUMERAL TWO: try adding symbols</li>
<li>U+2172 SMALL ROMAN NUMERAL THREE: try adding symbols</li>
<li>U+2173 SMALL ROMAN NUMERAL FOUR: try adding symbols</li>
<li>U+2174 SMALL ROMAN NUMERAL FIVE: try adding symbols</li>
<li>U+2175 SMALL ROMAN NUMERAL SIX: try adding symbols</li>
<li>U+2176 SMALL ROMAN NUMERAL SEVEN: try adding symbols</li>
<li>U+2177 SMALL ROMAN NUMERAL EIGHT: try adding symbols</li>
<li>U+2178 SMALL ROMAN NUMERAL NINE: try adding symbols</li>
<li>U+2179 SMALL ROMAN NUMERAL TEN: try adding symbols</li>
<li>U+217A SMALL ROMAN NUMERAL ELEVEN: try adding symbols</li>
<li>U+217B SMALL ROMAN NUMERAL TWELVE: try adding symbols</li>
<li>U+217C SMALL ROMAN NUMERAL FIFTY: try adding symbols</li>
<li>U+217D SMALL ROMAN NUMERAL ONE HUNDRED: try adding symbols</li>
<li>U+217E SMALL ROMAN NUMERAL FIVE HUNDRED: try adding symbols</li>
<li>U+217F SMALL ROMAN NUMERAL ONE THOUSAND: try adding symbols</li>
<li>U+2180 ROMAN NUMERAL ONE THOUSAND C D: try adding symbols</li>
<li>U+2181 ROMAN NUMERAL FIVE THOUSAND: try adding symbols</li>
<li>U+2182 ROMAN NUMERAL TEN THOUSAND: try adding symbols</li>
<li>U+2183 ROMAN NUMERAL REVERSED ONE HUNDRED: try adding symbols</li>
<li>U+2184 LATIN SMALL LETTER REVERSED C: not included in any glyphset definition</li>
<li>U+2185 ROMAN NUMERAL SIX LATE FORM: try adding symbols</li>
<li>U+2186 ROMAN NUMERAL FIFTY EARLY FORM: try adding symbols</li>
<li>U+2187 ROMAN NUMERAL FIFTY THOUSAND: try adding symbols</li>
<li>U+2188 ROMAN NUMERAL ONE HUNDRED THOUSAND: try adding symbols</li>
<li>U+2189 VULGAR FRACTION ZERO THIRDS: try adding symbols</li>
<li>U+218A TURNED DIGIT TWO: try adding symbols</li>
<li>U+218B TURNED DIGIT THREE: try adding symbols</li>
<li>U+2190 LEFTWARDS ARROW: try adding one of: symbols, math</li>
<li>U+2192 RIGHTWARDS ARROW: try adding one of: symbols, math</li>
<li>U+2194 LEFT RIGHT ARROW: try adding one of: symbols, math</li>
<li>U+2195 UP DOWN ARROW: try adding one of: symbols, math</li>
<li>U+2196 NORTH WEST ARROW: try adding one of: symbols, math</li>
<li>U+2197 NORTH EAST ARROW: try adding one of: symbols, math</li>
<li>U+2198 SOUTH EAST ARROW: try adding one of: symbols, math</li>
<li>U+2199 SOUTH WEST ARROW: try adding one of: symbols, math</li>
<li>U+219A LEFTWARDS ARROW WITH STROKE: try adding math</li>
<li>U+219B RIGHTWARDS ARROW WITH STROKE: try adding math</li>
<li>U+219C LEFTWARDS WAVE ARROW: try adding math</li>
<li>U+219D RIGHTWARDS WAVE ARROW: try adding math</li>
<li>U+219E LEFTWARDS TWO HEADED ARROW: try adding math</li>
<li>U+219F UPWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A0 RIGHTWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A1 DOWNWARDS TWO HEADED ARROW: try adding math</li>
<li>U+21A2 LEFTWARDS ARROW WITH TAIL: try adding math</li>
<li>U+21A3 RIGHTWARDS ARROW WITH TAIL: try adding math</li>
<li>U+21A4 LEFTWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A5 UPWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A6 RIGHTWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A7 DOWNWARDS ARROW FROM BAR: try adding math</li>
<li>U+21A8 UP DOWN ARROW WITH BASE: try adding math</li>
<li>U+21A9 LEFTWARDS ARROW WITH HOOK: try adding math</li>
<li>U+21AA RIGHTWARDS ARROW WITH HOOK: try adding math</li>
<li>U+21AB LEFTWARDS ARROW WITH LOOP: try adding math</li>
<li>U+21AC RIGHTWARDS ARROW WITH LOOP: try adding math</li>
<li>U+21AD LEFT RIGHT WAVE ARROW: try adding math</li>
<li>U+21AE LEFT RIGHT ARROW WITH STROKE: try adding math</li>
<li>U+21AF DOWNWARDS ZIGZAG ARROW: try adding symbols</li>
<li>U+21B0 UPWARDS ARROW WITH TIP LEFTWARDS: try adding math</li>
<li>U+21B1 UPWARDS ARROW WITH TIP RIGHTWARDS: try adding math</li>
<li>U+21B2 DOWNWARDS ARROW WITH TIP LEFTWARDS: try adding math</li>
<li>U+21B3 DOWNWARDS ARROW WITH TIP RIGHTWARDS: try adding math</li>
<li>U+21B4 RIGHTWARDS ARROW WITH CORNER DOWNWARDS: try adding math</li>
<li>U+21B5 DOWNWARDS ARROW WITH CORNER LEFTWARDS: try adding math</li>
<li>U+21B6 ANTICLOCKWISE TOP SEMICIRCLE ARROW: try adding math</li>
<li>U+21B7 CLOCKWISE TOP SEMICIRCLE ARROW: try adding math</li>
<li>U+21B8 NORTH WEST ARROW TO LONG BAR: try adding math</li>
<li>U+21B9 LEFTWARDS ARROW TO BAR OVER RIGHTWARDS ARROW TO BAR: try adding math</li>
<li>U+21BA ANTICLOCKWISE OPEN CIRCLE ARROW: try adding math</li>
<li>U+21BB CLOCKWISE OPEN CIRCLE ARROW: try adding math</li>
<li>U+21BC LEFTWARDS HARPOON WITH BARB UPWARDS: try adding math</li>
<li>U+21BD LEFTWARDS HARPOON WITH BARB DOWNWARDS: try adding math</li>
<li>U+21BE UPWARDS HARPOON WITH BARB RIGHTWARDS: try adding math</li>
<li>U+21BF UPWARDS HARPOON WITH BARB LEFTWARDS: try adding math</li>
<li>U+21C0 RIGHTWARDS HARPOON WITH BARB UPWARDS: try adding math</li>
<li>U+21C1 RIGHTWARDS HARPOON WITH BARB DOWNWARDS: try adding math</li>
<li>U+21C2 DOWNWARDS HARPOON WITH BARB RIGHTWARDS: try adding math</li>
<li>U+21C3 DOWNWARDS HARPOON WITH BARB LEFTWARDS: try adding math</li>
<li>U+21C4 RIGHTWARDS ARROW OVER LEFTWARDS ARROW: try adding math</li>
<li>U+21C5 UPWARDS ARROW LEFTWARDS OF DOWNWARDS ARROW: try adding math</li>
<li>U+21C6 LEFTWARDS ARROW OVER RIGHTWARDS ARROW: try adding math</li>
<li>U+21C7 LEFTWARDS PAIRED ARROWS: try adding math</li>
<li>U+21C8 UPWARDS PAIRED ARROWS: try adding math</li>
<li>U+21C9 RIGHTWARDS PAIRED ARROWS: try adding math</li>
<li>U+21CA DOWNWARDS PAIRED ARROWS: try adding math</li>
<li>U+21CB LEFTWARDS HARPOON OVER RIGHTWARDS HARPOON: try adding math</li>
<li>U+21CC RIGHTWARDS HARPOON OVER LEFTWARDS HARPOON: try adding math</li>
<li>U+21CD LEFTWARDS DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21CE LEFT RIGHT DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21CF RIGHTWARDS DOUBLE ARROW WITH STROKE: try adding math</li>
<li>U+21D0 LEFTWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D1 UPWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D2 RIGHTWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D3 DOWNWARDS DOUBLE ARROW: try adding math</li>
<li>U+21D4 LEFT RIGHT DOUBLE ARROW: try adding math</li>
<li>U+21D5 UP DOWN DOUBLE ARROW: try adding math</li>
<li>U+21D6 NORTH WEST DOUBLE ARROW: try adding math</li>
<li>U+21D7 NORTH EAST DOUBLE ARROW: try adding math</li>
<li>U+21D8 SOUTH EAST DOUBLE ARROW: try adding math</li>
<li>U+21D9 SOUTH WEST DOUBLE ARROW: try adding math</li>
<li>U+21DA LEFTWARDS TRIPLE ARROW: try adding math</li>
<li>U+21DB RIGHTWARDS TRIPLE ARROW: try adding math</li>
<li>U+21DC LEFTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+21DD RIGHTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+21DE UPWARDS ARROW WITH DOUBLE STROKE: try adding math</li>
<li>U+21DF DOWNWARDS ARROW WITH DOUBLE STROKE: try adding math</li>
<li>U+21E0 LEFTWARDS DASHED ARROW: try adding math</li>
<li>U+21E1 UPWARDS DASHED ARROW: try adding math</li>
<li>U+21E2 RIGHTWARDS DASHED ARROW: try adding math</li>
<li>U+21E3 DOWNWARDS DASHED ARROW: try adding math</li>
<li>U+21E4 LEFTWARDS ARROW TO BAR: try adding math</li>
<li>U+21E5 RIGHTWARDS ARROW TO BAR: try adding math</li>
<li>U+21E6 LEFTWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E7 UPWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E8 RIGHTWARDS WHITE ARROW: try adding symbols</li>
<li>U+21E9 DOWNWARDS WHITE ARROW: try adding symbols</li>
<li>U+21EA UPWARDS WHITE ARROW FROM BAR: try adding symbols</li>
<li>U+21EB UPWARDS WHITE ARROW ON PEDESTAL: try adding symbols</li>
<li>U+21EC UPWARDS WHITE ARROW ON PEDESTAL WITH HORIZONTAL BAR: try adding symbols</li>
<li>U+21ED UPWARDS WHITE ARROW ON PEDESTAL WITH VERTICAL BAR: try adding symbols</li>
<li>U+21EE UPWARDS WHITE DOUBLE ARROW: try adding symbols</li>
<li>U+21EF UPWARDS WHITE DOUBLE ARROW ON PEDESTAL: try adding symbols</li>
<li>U+21F0 RIGHTWARDS WHITE ARROW FROM WALL: try adding symbols</li>
<li>U+21F1 NORTH WEST ARROW TO CORNER: try adding math</li>
<li>U+21F2 SOUTH EAST ARROW TO CORNER: try adding math</li>
<li>U+21F3 UP DOWN WHITE ARROW: try adding symbols</li>
<li>U+21F4 RIGHT ARROW WITH SMALL CIRCLE: try adding math</li>
<li>U+21F5 DOWNWARDS ARROW LEFTWARDS OF UPWARDS ARROW: try adding math</li>
<li>U+21F6 THREE RIGHTWARDS ARROWS: try adding math</li>
<li>U+21F7 LEFTWARDS ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21F8 RIGHTWARDS ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21F9 LEFT RIGHT ARROW WITH VERTICAL STROKE: try adding math</li>
<li>U+21FA LEFTWARDS ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FB RIGHTWARDS ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FC LEFT RIGHT ARROW WITH DOUBLE VERTICAL STROKE: try adding math</li>
<li>U+21FD LEFTWARDS OPEN-HEADED ARROW: try adding math</li>
<li>U+21FE RIGHTWARDS OPEN-HEADED ARROW: try adding math</li>
<li>U+21FF LEFT RIGHT OPEN-HEADED ARROW: try adding math</li>
<li>U+2200 FOR ALL: try adding math</li>
<li>U+2201 COMPLEMENT: try adding math</li>
<li>U+2202 PARTIAL DIFFERENTIAL: try adding math</li>
<li>U+2203 THERE EXISTS: try adding math</li>
<li>U+2204 THERE DOES NOT EXIST: try adding math</li>
<li>U+2205 EMPTY SET: try adding math</li>
<li>U+2206 INCREMENT: try adding math</li>
<li>U+2207 NABLA: try adding math</li>
<li>U+2208 ELEMENT OF: try adding math</li>
<li>U+2209 NOT AN ELEMENT OF: try adding math</li>
<li>U+220A SMALL ELEMENT OF: try adding math</li>
<li>U+220B CONTAINS AS MEMBER: try adding math</li>
<li>U+220C DOES NOT CONTAIN AS MEMBER: try adding math</li>
<li>U+220D SMALL CONTAINS AS MEMBER: try adding math</li>
<li>U+220E END OF PROOF: try adding math</li>
<li>U+220F N-ARY PRODUCT: try adding math</li>
<li>U+2210 N-ARY COPRODUCT: try adding math</li>
<li>U+2211 N-ARY SUMMATION: try adding math</li>
<li>U+2213 MINUS-OR-PLUS SIGN: try adding math</li>
<li>U+2214 DOT PLUS: try adding math</li>
<li>U+2216 SET MINUS: try adding math</li>
<li>U+2217 ASTERISK OPERATOR: try adding math</li>
<li>U+2218 RING OPERATOR: try adding one of: symbols, math</li>
<li>U+2219 BULLET OPERATOR: try adding one of: tai-tham, symbols, math, yi</li>
<li>U+221A SQUARE ROOT: try adding math</li>
<li>U+221B CUBE ROOT: try adding math</li>
<li>U+221C FOURTH ROOT: try adding math</li>
<li>U+221D PROPORTIONAL TO: try adding math</li>
<li>U+221E INFINITY: try adding math</li>
<li>U+221F RIGHT ANGLE: try adding math</li>
<li>U+2220 ANGLE: try adding math</li>
<li>U+2221 MEASURED ANGLE: try adding math</li>
<li>U+2222 SPHERICAL ANGLE: try adding math</li>
<li>U+2223 DIVIDES: try adding math</li>
<li>U+2224 DOES NOT DIVIDE: try adding math</li>
<li>U+2225 PARALLEL TO: try adding math</li>
<li>U+2226 NOT PARALLEL TO: try adding math</li>
<li>U+2227 LOGICAL AND: try adding math</li>
<li>U+2228 LOGICAL OR: try adding math</li>
<li>U+2229 INTERSECTION: try adding math</li>
<li>U+222A UNION: try adding math</li>
<li>U+222B INTEGRAL: try adding math</li>
<li>U+222C DOUBLE INTEGRAL: try adding math</li>
<li>U+222D TRIPLE INTEGRAL: try adding math</li>
<li>U+222E CONTOUR INTEGRAL: try adding math</li>
<li>U+222F SURFACE INTEGRAL: try adding math</li>
<li>U+2230 VOLUME INTEGRAL: try adding math</li>
<li>U+2231 CLOCKWISE INTEGRAL: try adding math</li>
<li>U+2232 CLOCKWISE CONTOUR INTEGRAL: try adding math</li>
<li>U+2233 ANTICLOCKWISE CONTOUR INTEGRAL: try adding math</li>
<li>U+2234 THEREFORE: try adding math</li>
<li>U+2235 BECAUSE: try adding math</li>
<li>U+2236 RATIO: try adding math</li>
<li>U+2237 PROPORTION: try adding math</li>
<li>U+2238 DOT MINUS: try adding math</li>
<li>U+2239 EXCESS: try adding math</li>
<li>U+223A GEOMETRIC PROPORTION: try adding math</li>
<li>U+223B HOMOTHETIC: try adding math</li>
<li>U+223C TILDE OPERATOR: try adding math</li>
<li>U+223D REVERSED TILDE: try adding math</li>
<li>U+223E INVERTED LAZY S: try adding math</li>
<li>U+223F SINE WAVE: try adding math</li>
<li>U+2240 WREATH PRODUCT: try adding math</li>
<li>U+2241 NOT TILDE: try adding math</li>
<li>U+2242 MINUS TILDE: try adding math</li>
<li>U+2243 ASYMPTOTICALLY EQUAL TO: try adding math</li>
<li>U+2244 NOT ASYMPTOTICALLY EQUAL TO: try adding math</li>
<li>U+2245 APPROXIMATELY EQUAL TO: try adding math</li>
<li>U+2246 APPROXIMATELY BUT NOT ACTUALLY EQUAL TO: try adding math</li>
<li>U+2247 NEITHER APPROXIMATELY NOR ACTUALLY EQUAL TO: try adding math</li>
<li>U+2248 ALMOST EQUAL TO: try adding math</li>
<li>U+2249 NOT ALMOST EQUAL TO: try adding math</li>
<li>U+224A ALMOST EQUAL OR EQUAL TO: try adding math</li>
<li>U+224B TRIPLE TILDE: try adding math</li>
<li>U+224C ALL EQUAL TO: try adding math</li>
<li>U+224D EQUIVALENT TO: try adding math</li>
<li>U+224E GEOMETRICALLY EQUIVALENT TO: try adding math</li>
<li>U+224F DIFFERENCE BETWEEN: try adding math</li>
<li>U+2250 APPROACHES THE LIMIT: try adding math</li>
<li>U+2251 GEOMETRICALLY EQUAL TO: try adding math</li>
<li>U+2252 APPROXIMATELY EQUAL TO OR THE IMAGE OF: try adding math</li>
<li>U+2253 IMAGE OF OR APPROXIMATELY EQUAL TO: try adding math</li>
<li>U+2254 COLON EQUALS: try adding math</li>
<li>U+2255 EQUALS COLON: try adding math</li>
<li>U+2256 RING IN EQUAL TO: try adding math</li>
<li>U+2257 RING EQUAL TO: try adding math</li>
<li>U+2258 CORRESPONDS TO: try adding math</li>
<li>U+2259 ESTIMATES: try adding math</li>
<li>U+225A EQUIANGULAR TO: try adding math</li>
<li>U+225B STAR EQUALS: try adding math</li>
<li>U+225C DELTA EQUAL TO: try adding math</li>
<li>U+225D EQUAL TO BY DEFINITION: try adding math</li>
<li>U+225E MEASURED BY: try adding math</li>
<li>U+225F QUESTIONED EQUAL TO: try adding math</li>
<li>U+2260 NOT EQUAL TO: try adding math</li>
<li>U+2261 IDENTICAL TO: try adding math</li>
<li>U+2262 NOT IDENTICAL TO: try adding math</li>
<li>U+2263 STRICTLY EQUIVALENT TO: try adding math</li>
<li>U+2264 LESS-THAN OR EQUAL TO: try adding math</li>
<li>U+2265 GREATER-THAN OR EQUAL TO: try adding math</li>
<li>U+2266 LESS-THAN OVER EQUAL TO: try adding math</li>
<li>U+2267 GREATER-THAN OVER EQUAL TO: try adding math</li>
<li>U+2268 LESS-THAN BUT NOT EQUAL TO: try adding math</li>
<li>U+2269 GREATER-THAN BUT NOT EQUAL TO: try adding math</li>
<li>U+226A MUCH LESS-THAN: try adding math</li>
<li>U+226B MUCH GREATER-THAN: try adding math</li>
<li>U+226C BETWEEN: try adding math</li>
<li>U+226D NOT EQUIVALENT TO: try adding math</li>
<li>U+226E NOT LESS-THAN: try adding math</li>
<li>U+226F NOT GREATER-THAN: try adding math</li>
<li>U+2270 NEITHER LESS-THAN NOR EQUAL TO: try adding math</li>
<li>U+2271 NEITHER GREATER-THAN NOR EQUAL TO: try adding math</li>
<li>U+2272 LESS-THAN OR EQUIVALENT TO: try adding math</li>
<li>U+2273 GREATER-THAN OR EQUIVALENT TO: try adding math</li>
<li>U+2274 NEITHER LESS-THAN NOR EQUIVALENT TO: try adding math</li>
<li>U+2275 NEITHER GREATER-THAN NOR EQUIVALENT TO: try adding math</li>
<li>U+2276 LESS-THAN OR GREATER-THAN: try adding math</li>
<li>U+2277 GREATER-THAN OR LESS-THAN: try adding math</li>
<li>U+2278 NEITHER LESS-THAN NOR GREATER-THAN: try adding math</li>
<li>U+2279 NEITHER GREATER-THAN NOR LESS-THAN: try adding math</li>
<li>U+227A PRECEDES: try adding math</li>
<li>U+227B SUCCEEDS: try adding math</li>
<li>U+227C PRECEDES OR EQUAL TO: try adding math</li>
<li>U+227D SUCCEEDS OR EQUAL TO: try adding math</li>
<li>U+227E PRECEDES OR EQUIVALENT TO: try adding math</li>
<li>U+227F SUCCEEDS OR EQUIVALENT TO: try adding math</li>
<li>U+2280 DOES NOT PRECEDE: try adding math</li>
<li>U+2281 DOES NOT SUCCEED: try adding math</li>
<li>U+2282 SUBSET OF: try adding math</li>
<li>U+2283 SUPERSET OF: try adding math</li>
<li>U+2284 NOT A SUBSET OF: try adding math</li>
<li>U+2285 NOT A SUPERSET OF: try adding math</li>
<li>U+2286 SUBSET OF OR EQUAL TO: try adding math</li>
<li>U+2287 SUPERSET OF OR EQUAL TO: try adding math</li>
<li>U+2288 NEITHER A SUBSET OF NOR EQUAL TO: try adding math</li>
<li>U+2289 NEITHER A SUPERSET OF NOR EQUAL TO: try adding math</li>
<li>U+228A SUBSET OF WITH NOT EQUAL TO: try adding math</li>
<li>U+228B SUPERSET OF WITH NOT EQUAL TO: try adding math</li>
<li>U+228C MULTISET: try adding math</li>
<li>U+228D MULTISET MULTIPLICATION: try adding math</li>
<li>U+228E MULTISET UNION: try adding math</li>
<li>U+228F SQUARE IMAGE OF: try adding math</li>
<li>U+2290 SQUARE ORIGINAL OF: try adding math</li>
<li>U+2291 SQUARE IMAGE OF OR EQUAL TO: try adding math</li>
<li>U+2292 SQUARE ORIGINAL OF OR EQUAL TO: try adding math</li>
<li>U+2293 SQUARE CAP: try adding math</li>
<li>U+2294 SQUARE CUP: try adding math</li>
<li>U+2295 CIRCLED PLUS: try adding math</li>
<li>U+2296 CIRCLED MINUS: try adding math</li>
<li>U+2297 CIRCLED TIMES: try adding math</li>
<li>U+2298 CIRCLED DIVISION SLASH: try adding math</li>
<li>U+2299 CIRCLED DOT OPERATOR: try adding one of: symbols, math</li>
<li>U+229A CIRCLED RING OPERATOR: try adding math</li>
<li>U+229B CIRCLED ASTERISK OPERATOR: try adding math</li>
<li>U+229C CIRCLED EQUALS: try adding math</li>
<li>U+229D CIRCLED DASH: try adding math</li>
<li>U+229E SQUARED PLUS: try adding math</li>
<li>U+229F SQUARED MINUS: try adding math</li>
<li>U+22A0 SQUARED TIMES: try adding math</li>
<li>U+22A1 SQUARED DOT OPERATOR: try adding math</li>
<li>U+22A2 RIGHT TACK: try adding math</li>
<li>U+22A3 LEFT TACK: try adding math</li>
<li>U+22A4 DOWN TACK: try adding math</li>
<li>U+22A5 UP TACK: try adding math</li>
<li>U+22A6 ASSERTION: try adding math</li>
<li>U+22A7 MODELS: try adding math</li>
<li>U+22A8 TRUE: try adding math</li>
<li>U+22A9 FORCES: try adding math</li>
<li>U+22AA TRIPLE VERTICAL BAR RIGHT TURNSTILE: try adding math</li>
<li>U+22AB DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE: try adding math</li>
<li>U+22AC DOES NOT PROVE: try adding math</li>
<li>U+22AD NOT TRUE: try adding math</li>
<li>U+22AE DOES NOT FORCE: try adding math</li>
<li>U+22AF NEGATED DOUBLE VERTICAL BAR DOUBLE RIGHT TURNSTILE: try adding math</li>
<li>U+22B0 PRECEDES UNDER RELATION: try adding math</li>
<li>U+22B1 SUCCEEDS UNDER RELATION: try adding math</li>
<li>U+22B2 NORMAL SUBGROUP OF: try adding math</li>
<li>U+22B3 CONTAINS AS NORMAL SUBGROUP: try adding math</li>
<li>U+22B4 NORMAL SUBGROUP OF OR EQUAL TO: try adding math</li>
<li>U+22B5 CONTAINS AS NORMAL SUBGROUP OR EQUAL TO: try adding math</li>
<li>U+22B6 ORIGINAL OF: try adding math</li>
<li>U+22B7 IMAGE OF: try adding math</li>
<li>U+22B8 MULTIMAP: try adding math</li>
<li>U+22B9 HERMITIAN CONJUGATE MATRIX: try adding math</li>
<li>U+22BA INTERCALATE: try adding math</li>
<li>U+22BB XOR: try adding math</li>
<li>U+22BC NAND: try adding math</li>
<li>U+22BD NOR: try adding math</li>
<li>U+22BE RIGHT ANGLE WITH ARC: try adding math</li>
<li>U+22BF RIGHT TRIANGLE: try adding math</li>
<li>U+22C0 N-ARY LOGICAL AND: try adding math</li>
<li>U+22C1 N-ARY LOGICAL OR: try adding math</li>
<li>U+22C2 N-ARY INTERSECTION: try adding math</li>
<li>U+22C3 N-ARY UNION: try adding math</li>
<li>U+22C4 DIAMOND OPERATOR: try adding one of: symbols, math</li>
<li>U+22C5 DOT OPERATOR: try adding one of: symbols, math</li>
<li>U+22C6 STAR OPERATOR: try adding one of: symbols, math</li>
<li>U+22C7 DIVISION TIMES: try adding math</li>
<li>U+22C8 BOWTIE: try adding math</li>
<li>U+22C9 LEFT NORMAL FACTOR SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CA RIGHT NORMAL FACTOR SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CB LEFT SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CC RIGHT SEMIDIRECT PRODUCT: try adding math</li>
<li>U+22CD REVERSED TILDE EQUALS: try adding math</li>
<li>U+22CE CURLY LOGICAL OR: try adding math</li>
<li>U+22CF CURLY LOGICAL AND: try adding math</li>
<li>U+22D0 DOUBLE SUBSET: try adding math</li>
<li>U+22D1 DOUBLE SUPERSET: try adding math</li>
<li>U+22D2 DOUBLE INTERSECTION: try adding math</li>
<li>U+22D3 DOUBLE UNION: try adding math</li>
<li>U+22D4 PITCHFORK: try adding math</li>
<li>U+22D5 EQUAL AND PARALLEL TO: try adding math</li>
<li>U+22D6 LESS-THAN WITH DOT: try adding math</li>
<li>U+22D7 GREATER-THAN WITH DOT: try adding math</li>
<li>U+22D8 VERY MUCH LESS-THAN: try adding math</li>
<li>U+22D9 VERY MUCH GREATER-THAN: try adding math</li>
<li>U+22DA LESS-THAN EQUAL TO OR GREATER-THAN: try adding math</li>
<li>U+22DB GREATER-THAN EQUAL TO OR LESS-THAN: try adding math</li>
<li>U+22DC EQUAL TO OR LESS-THAN: try adding math</li>
<li>U+22DD EQUAL TO OR GREATER-THAN: try adding math</li>
<li>U+22DE EQUAL TO OR PRECEDES: try adding math</li>
<li>U+22DF EQUAL TO OR SUCCEEDS: try adding math</li>
<li>U+22E0 DOES NOT PRECEDE OR EQUAL: try adding math</li>
<li>U+22E1 DOES NOT SUCCEED OR EQUAL: try adding math</li>
<li>U+22E2 NOT SQUARE IMAGE OF OR EQUAL TO: try adding math</li>
<li>U+22E3 NOT SQUARE ORIGINAL OF OR EQUAL TO: try adding math</li>
<li>U+22E4 SQUARE IMAGE OF OR NOT EQUAL TO: try adding math</li>
<li>U+22E5 SQUARE ORIGINAL OF OR NOT EQUAL TO: try adding math</li>
<li>U+22E6 LESS-THAN BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E7 GREATER-THAN BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E8 PRECEDES BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22E9 SUCCEEDS BUT NOT EQUIVALENT TO: try adding math</li>
<li>U+22EA NOT NORMAL SUBGROUP OF: try adding math</li>
<li>U+22EB DOES NOT CONTAIN AS NORMAL SUBGROUP: try adding math</li>
<li>U+22EC NOT NORMAL SUBGROUP OF OR EQUAL TO: try adding math</li>
<li>U+22ED DOES NOT CONTAIN AS NORMAL SUBGROUP OR EQUAL: try adding math</li>
<li>U+22EE VERTICAL ELLIPSIS: try adding math</li>
<li>U+22EF MIDLINE HORIZONTAL ELLIPSIS: try adding math</li>
<li>U+22F0 UP RIGHT DIAGONAL ELLIPSIS: try adding math</li>
<li>U+22F1 DOWN RIGHT DIAGONAL ELLIPSIS: try adding math</li>
<li>U+22F2 ELEMENT OF WITH LONG HORIZONTAL STROKE: try adding math</li>
<li>U+22F3 ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22F4 SMALL ELEMENT OF WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22F5 ELEMENT OF WITH DOT ABOVE: try adding math</li>
<li>U+22F6 ELEMENT OF WITH OVERBAR: try adding math</li>
<li>U+22F7 SMALL ELEMENT OF WITH OVERBAR: try adding math</li>
<li>U+22F8 ELEMENT OF WITH UNDERBAR: try adding math</li>
<li>U+22F9 ELEMENT OF WITH TWO HORIZONTAL STROKES: try adding math</li>
<li>U+22FA CONTAINS WITH LONG HORIZONTAL STROKE: try adding math</li>
<li>U+22FB CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22FC SMALL CONTAINS WITH VERTICAL BAR AT END OF HORIZONTAL STROKE: try adding math</li>
<li>U+22FD CONTAINS WITH OVERBAR: try adding math</li>
<li>U+22FE SMALL CONTAINS WITH OVERBAR: try adding math</li>
<li>U+22FF Z NOTATION BAG MEMBERSHIP: try adding math</li>
<li>U+2460 CIRCLED DIGIT ONE: try adding one of: yi, symbols, mongolian</li>
<li>U+2461 CIRCLED DIGIT TWO: try adding one of: yi, symbols, mongolian</li>
<li>U+2462 CIRCLED DIGIT THREE: try adding one of: yi, symbols, mongolian</li>
<li>U+2463 CIRCLED DIGIT FOUR: try adding one of: yi, symbols, mongolian</li>
<li>U+2464 CIRCLED DIGIT FIVE: try adding one of: yi, symbols, mongolian</li>
<li>U+2465 CIRCLED DIGIT SIX: try adding one of: yi, symbols, mongolian</li>
<li>U+2466 CIRCLED DIGIT SEVEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2467 CIRCLED DIGIT EIGHT: try adding one of: yi, symbols, mongolian</li>
<li>U+2468 CIRCLED DIGIT NINE: try adding one of: yi, symbols, mongolian</li>
<li>U+2469 CIRCLED NUMBER TEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246A CIRCLED NUMBER ELEVEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246B CIRCLED NUMBER TWELVE: try adding one of: yi, symbols, mongolian</li>
<li>U+246C CIRCLED NUMBER THIRTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246D CIRCLED NUMBER FOURTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246E CIRCLED NUMBER FIFTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+246F CIRCLED NUMBER SIXTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2470 CIRCLED NUMBER SEVENTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2471 CIRCLED NUMBER EIGHTEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2472 CIRCLED NUMBER NINETEEN: try adding one of: yi, symbols, mongolian</li>
<li>U+2473 CIRCLED NUMBER TWENTY: try adding one of: yi, symbols, mongolian</li>
<li>U+2474 PARENTHESIZED DIGIT ONE: try adding one of: symbols, math</li>
<li>U+2475 PARENTHESIZED DIGIT TWO: try adding one of: symbols, math</li>
<li>U+2476 PARENTHESIZED DIGIT THREE: try adding symbols</li>
<li>U+2477 PARENTHESIZED DIGIT FOUR: try adding symbols</li>
<li>U+2478 PARENTHESIZED DIGIT FIVE: try adding symbols</li>
<li>U+2479 PARENTHESIZED DIGIT SIX: try adding symbols</li>
<li>U+247A PARENTHESIZED DIGIT SEVEN: try adding symbols</li>
<li>U+247B PARENTHESIZED DIGIT EIGHT: try adding symbols</li>
<li>U+247C PARENTHESIZED DIGIT NINE: try adding symbols</li>
<li>U+247D PARENTHESIZED NUMBER TEN: try adding symbols</li>
<li>U+247E PARENTHESIZED NUMBER ELEVEN: try adding symbols</li>
<li>U+247F PARENTHESIZED NUMBER TWELVE: try adding symbols</li>
<li>U+2480 PARENTHESIZED NUMBER THIRTEEN: try adding symbols</li>
<li>U+2481 PARENTHESIZED NUMBER FOURTEEN: try adding symbols</li>
<li>U+2482 PARENTHESIZED NUMBER FIFTEEN: try adding symbols</li>
<li>U+2483 PARENTHESIZED NUMBER SIXTEEN: try adding symbols</li>
<li>U+2484 PARENTHESIZED NUMBER SEVENTEEN: try adding symbols</li>
<li>U+2485 PARENTHESIZED NUMBER EIGHTEEN: try adding symbols</li>
<li>U+2486 PARENTHESIZED NUMBER NINETEEN: try adding symbols</li>
<li>U+2487 PARENTHESIZED NUMBER TWENTY: try adding symbols</li>
<li>U+2488 DIGIT ONE FULL STOP: try adding symbols</li>
<li>U+2489 DIGIT TWO FULL STOP: try adding symbols</li>
<li>U+248A DIGIT THREE FULL STOP: try adding symbols</li>
<li>U+248B DIGIT FOUR FULL STOP: try adding symbols</li>
<li>U+248C DIGIT FIVE FULL STOP: try adding symbols</li>
<li>U+248D DIGIT SIX FULL STOP: try adding symbols</li>
<li>U+248E DIGIT SEVEN FULL STOP: try adding symbols</li>
<li>U+248F DIGIT EIGHT FULL STOP: try adding symbols</li>
<li>U+2490 DIGIT NINE FULL STOP: try adding symbols</li>
<li>U+2491 NUMBER TEN FULL STOP: try adding symbols</li>
<li>U+2492 NUMBER ELEVEN FULL STOP: try adding symbols</li>
<li>U+2493 NUMBER TWELVE FULL STOP: try adding symbols</li>
<li>U+2494 NUMBER THIRTEEN FULL STOP: try adding symbols</li>
<li>U+2495 NUMBER FOURTEEN FULL STOP: try adding symbols</li>
<li>U+2496 NUMBER FIFTEEN FULL STOP: try adding symbols</li>
<li>U+2497 NUMBER SIXTEEN FULL STOP: try adding symbols</li>
<li>U+2498 NUMBER SEVENTEEN FULL STOP: try adding symbols</li>
<li>U+2499 NUMBER EIGHTEEN FULL STOP: try adding symbols</li>
<li>U+249A NUMBER NINETEEN FULL STOP: try adding symbols</li>
<li>U+249B NUMBER TWENTY FULL STOP: try adding symbols</li>
<li>U+249C PARENTHESIZED LATIN SMALL LETTER A: try adding symbols</li>
<li>U+249D PARENTHESIZED LATIN SMALL LETTER B: try adding symbols</li>
<li>U+249E PARENTHESIZED LATIN SMALL LETTER C: try adding symbols</li>
<li>U+249F PARENTHESIZED LATIN SMALL LETTER D: try adding symbols</li>
<li>U+24A0 PARENTHESIZED LATIN SMALL LETTER E: try adding symbols</li>
<li>U+24A1 PARENTHESIZED LATIN SMALL LETTER F: try adding symbols</li>
<li>U+24A2 PARENTHESIZED LATIN SMALL LETTER G: try adding symbols</li>
<li>U+24A3 PARENTHESIZED LATIN SMALL LETTER H: try adding symbols</li>
<li>U+24A4 PARENTHESIZED LATIN SMALL LETTER I: try adding symbols</li>
<li>U+24A5 PARENTHESIZED LATIN SMALL LETTER J: try adding symbols</li>
<li>U+24A6 PARENTHESIZED LATIN SMALL LETTER K: try adding symbols</li>
<li>U+24A7 PARENTHESIZED LATIN SMALL LETTER L: try adding symbols</li>
<li>U+24A8 PARENTHESIZED LATIN SMALL LETTER M: try adding symbols</li>
<li>U+24A9 PARENTHESIZED LATIN SMALL LETTER N: try adding symbols</li>
<li>U+24AA PARENTHESIZED LATIN SMALL LETTER O: try adding symbols</li>
<li>U+24AB PARENTHESIZED LATIN SMALL LETTER P: try adding symbols</li>
<li>U+24AC PARENTHESIZED LATIN SMALL LETTER Q: try adding symbols</li>
<li>U+24AD PARENTHESIZED LATIN SMALL LETTER R: try adding symbols</li>
<li>U+24AE PARENTHESIZED LATIN SMALL LETTER S: try adding symbols</li>
<li>U+24AF PARENTHESIZED LATIN SMALL LETTER T: try adding symbols</li>
<li>U+24B0 PARENTHESIZED LATIN SMALL LETTER U: try adding symbols</li>
<li>U+24B1 PARENTHESIZED LATIN SMALL LETTER V: try adding symbols</li>
<li>U+24B2 PARENTHESIZED LATIN SMALL LETTER W: try adding symbols</li>
<li>U+24B3 PARENTHESIZED LATIN SMALL LETTER X: try adding symbols</li>
<li>U+24B4 PARENTHESIZED LATIN SMALL LETTER Y: try adding symbols</li>
<li>U+24B5 PARENTHESIZED LATIN SMALL LETTER Z: try adding symbols</li>
<li>U+24B6 CIRCLED LATIN CAPITAL LETTER A: try adding symbols</li>
<li>U+24B7 CIRCLED LATIN CAPITAL LETTER B: try adding symbols</li>
<li>U+24B8 CIRCLED LATIN CAPITAL LETTER C: try adding symbols</li>
<li>U+24B9 CIRCLED LATIN CAPITAL LETTER D: try adding symbols</li>
<li>U+24BA CIRCLED LATIN CAPITAL LETTER E: try adding symbols</li>
<li>U+24BB CIRCLED LATIN CAPITAL LETTER F: try adding symbols</li>
<li>U+24BC CIRCLED LATIN CAPITAL LETTER G: try adding symbols</li>
<li>U+24BD CIRCLED LATIN CAPITAL LETTER H: try adding symbols</li>
<li>U+24BE CIRCLED LATIN CAPITAL LETTER I: try adding symbols</li>
<li>U+24BF CIRCLED LATIN CAPITAL LETTER J: try adding symbols</li>
<li>U+24C0 CIRCLED LATIN CAPITAL LETTER K: try adding symbols</li>
<li>U+24C1 CIRCLED LATIN CAPITAL LETTER L: try adding symbols</li>
<li>U+24C2 CIRCLED LATIN CAPITAL LETTER M: try adding symbols</li>
<li>U+24C3 CIRCLED LATIN CAPITAL LETTER N: try adding symbols</li>
<li>U+24C4 CIRCLED LATIN CAPITAL LETTER O: try adding symbols</li>
<li>U+24C5 CIRCLED LATIN CAPITAL LETTER P: try adding symbols</li>
<li>U+24C6 CIRCLED LATIN CAPITAL LETTER Q: try adding symbols</li>
<li>U+24C7 CIRCLED LATIN CAPITAL LETTER R: try adding symbols</li>
<li>U+24C8 CIRCLED LATIN CAPITAL LETTER S: try adding symbols</li>
<li>U+24C9 CIRCLED LATIN CAPITAL LETTER T: try adding symbols</li>
<li>U+24CA CIRCLED LATIN CAPITAL LETTER U: try adding symbols</li>
<li>U+24CB CIRCLED LATIN CAPITAL LETTER V: try adding symbols</li>
<li>U+24CC CIRCLED LATIN CAPITAL LETTER W: try adding symbols</li>
<li>U+24CD CIRCLED LATIN CAPITAL LETTER X: try adding symbols</li>
<li>U+24CE CIRCLED LATIN CAPITAL LETTER Y: try adding symbols</li>
<li>U+24CF CIRCLED LATIN CAPITAL LETTER Z: try adding symbols</li>
<li>U+24D0 CIRCLED LATIN SMALL LETTER A: try adding symbols</li>
<li>U+24D1 CIRCLED LATIN SMALL LETTER B: try adding symbols</li>
<li>U+24D2 CIRCLED LATIN SMALL LETTER C: try adding symbols</li>
<li>U+24D3 CIRCLED LATIN SMALL LETTER D: try adding symbols</li>
<li>U+24D4 CIRCLED LATIN SMALL LETTER E: try adding symbols</li>
<li>U+24D5 CIRCLED LATIN SMALL LETTER F: try adding symbols</li>
<li>U+24D6 CIRCLED LATIN SMALL LETTER G: try adding symbols</li>
<li>U+24D7 CIRCLED LATIN SMALL LETTER H: try adding symbols</li>
<li>U+24D8 CIRCLED LATIN SMALL LETTER I: try adding symbols</li>
<li>U+24D9 CIRCLED LATIN SMALL LETTER J: try adding symbols</li>
<li>U+24DA CIRCLED LATIN SMALL LETTER K: try adding symbols</li>
<li>U+24DB CIRCLED LATIN SMALL LETTER L: try adding symbols</li>
<li>U+24DC CIRCLED LATIN SMALL LETTER M: try adding symbols</li>
<li>U+24DD CIRCLED LATIN SMALL LETTER N: try adding symbols</li>
<li>U+24DE CIRCLED LATIN SMALL LETTER O: try adding symbols</li>
<li>U+24DF CIRCLED LATIN SMALL LETTER P: try adding symbols</li>
<li>U+24E0 CIRCLED LATIN SMALL LETTER Q: try adding symbols</li>
<li>U+24E1 CIRCLED LATIN SMALL LETTER R: try adding symbols</li>
<li>U+24E2 CIRCLED LATIN SMALL LETTER S: try adding symbols</li>
<li>U+24E3 CIRCLED LATIN SMALL LETTER T: try adding symbols</li>
<li>U+24E4 CIRCLED LATIN SMALL LETTER U: try adding symbols</li>
<li>U+24E5 CIRCLED LATIN SMALL LETTER V: try adding symbols</li>
<li>U+24E6 CIRCLED LATIN SMALL LETTER W: try adding symbols</li>
<li>U+24E7 CIRCLED LATIN SMALL LETTER X: try adding symbols</li>
<li>U+24E8 CIRCLED LATIN SMALL LETTER Y: try adding symbols</li>
<li>U+24E9 CIRCLED LATIN SMALL LETTER Z: try adding symbols</li>
<li>U+24EA CIRCLED DIGIT ZERO: try adding symbols</li>
<li>U+24EB NEGATIVE CIRCLED NUMBER ELEVEN: try adding symbols</li>
<li>U+24EC NEGATIVE CIRCLED NUMBER TWELVE: try adding symbols</li>
<li>U+24ED NEGATIVE CIRCLED NUMBER THIRTEEN: try adding symbols</li>
<li>U+24EE NEGATIVE CIRCLED NUMBER FOURTEEN: try adding symbols</li>
<li>U+24EF NEGATIVE CIRCLED NUMBER FIFTEEN: try adding symbols</li>
<li>U+24F0 NEGATIVE CIRCLED NUMBER SIXTEEN: try adding symbols</li>
<li>U+24F1 NEGATIVE CIRCLED NUMBER SEVENTEEN: try adding symbols</li>
<li>U+24F2 NEGATIVE CIRCLED NUMBER EIGHTEEN: try adding symbols</li>
<li>U+24F3 NEGATIVE CIRCLED NUMBER NINETEEN: try adding symbols</li>
<li>U+24F4 NEGATIVE CIRCLED NUMBER TWENTY: try adding symbols</li>
<li>U+24F5 DOUBLE CIRCLED DIGIT ONE: try adding symbols</li>
<li>U+24F6 DOUBLE CIRCLED DIGIT TWO: try adding symbols</li>
<li>U+24F7 DOUBLE CIRCLED DIGIT THREE: try adding symbols</li>
<li>U+24F8 DOUBLE CIRCLED DIGIT FOUR: try adding symbols</li>
<li>U+24F9 DOUBLE CIRCLED DIGIT FIVE: try adding symbols</li>
<li>U+24FA DOUBLE CIRCLED DIGIT SIX: try adding symbols</li>
<li>U+24FB DOUBLE CIRCLED DIGIT SEVEN: try adding symbols</li>
<li>U+24FC DOUBLE CIRCLED DIGIT EIGHT: try adding symbols</li>
<li>U+24FD DOUBLE CIRCLED DIGIT NINE: try adding symbols</li>
<li>U+24FE DOUBLE CIRCLED NUMBER TEN: try adding symbols</li>
<li>U+24FF NEGATIVE CIRCLED DIGIT ZERO: try adding symbols</li>
<li>U+25CC DOTTED CIRCLE: try adding one of: syriac, armenian, tai-le, tamil, zanabazar-square, coptic, mende-kikakui, khudawadi, gujarati, kayah-li, music, mandaic, elbasan, manichaean, soyombo, tagbanwa, thaana, hanunoo, khojki, devanagari, tifinagh, meetei-mayek, pahawh-hmong, sharada, oriya, newa, kharoshthi, buhid, phags-pa, bassa-vah, balinese, canadian-aboriginal, kannada, symbols, psalter-pahlavi, bhaiksuki, rejang, old-permic, syloti-nagri, warang-citi, kaithi, siddham, sogdian, khmer, saurashtra, ahom, batak, new-tai-lue, dogra, math, sundanese, mongolian, lepcha, nko, tibetan, buginese, sinhala, caucasian-albanian, myanmar, malayalam, osage, tirhuta, lao, javanese, thai, chakma, mahajani, modi, masaram-gondi, brahmi, hanifi-rohingya, duployan, takri, miao, limbu, tagalog, tai-viet, telugu, yi, gurmukhi, wancho, marchen, hebrew, grantha, gunjala-gondi, bengali, adlam, cham, tai-tham</li>
<li>U+25CF BLACK CIRCLE: try adding symbols</li>
<li>U+25EF LARGE CIRCLE: try adding symbols</li>
<li>U+2776 DINGBAT NEGATIVE CIRCLED DIGIT ONE: try adding symbols</li>
<li>U+2777 DINGBAT NEGATIVE CIRCLED DIGIT TWO: try adding symbols</li>
<li>U+2778 DINGBAT NEGATIVE CIRCLED DIGIT THREE: try adding symbols</li>
<li>U+2779 DINGBAT NEGATIVE CIRCLED DIGIT FOUR: try adding symbols</li>
<li>U+277A DINGBAT NEGATIVE CIRCLED DIGIT FIVE: try adding symbols</li>
<li>U+277B DINGBAT NEGATIVE CIRCLED DIGIT SIX: try adding symbols</li>
<li>U+277C DINGBAT NEGATIVE CIRCLED DIGIT SEVEN: try adding symbols</li>
<li>U+277D DINGBAT NEGATIVE CIRCLED DIGIT EIGHT: try adding symbols</li>
<li>U+277E DINGBAT NEGATIVE CIRCLED DIGIT NINE: try adding symbols</li>
<li>U+277F DINGBAT NEGATIVE CIRCLED NUMBER TEN: try adding symbols</li>
<li>U+27E8 MATHEMATICAL LEFT ANGLE BRACKET: try adding math</li>
<li>U+27E9 MATHEMATICAL RIGHT ANGLE BRACKET: try adding math</li>
<li>U+27EA MATHEMATICAL LEFT DOUBLE ANGLE BRACKET: try adding math</li>
<li>U+27EB MATHEMATICAL RIGHT DOUBLE ANGLE BRACKET: try adding math</li>
<li>U+27F2 ANTICLOCKWISE GAPPED CIRCLE ARROW: try adding math</li>
<li>U+27F3 CLOCKWISE GAPPED CIRCLE ARROW: try adding math</li>
<li>U+27F4 RIGHT ARROW WITH CIRCLED PLUS: try adding math</li>
<li>U+27F5 LONG LEFTWARDS ARROW: try adding math</li>
<li>U+27F6 LONG RIGHTWARDS ARROW: try adding math</li>
<li>U+27F7 LONG LEFT RIGHT ARROW: try adding math</li>
<li>U+27F8 LONG LEFTWARDS DOUBLE ARROW: try adding math</li>
<li>U+27F9 LONG RIGHTWARDS DOUBLE ARROW: try adding math</li>
<li>U+27FA LONG LEFT RIGHT DOUBLE ARROW: try adding math</li>
<li>U+27FB LONG LEFTWARDS ARROW FROM BAR: try adding math</li>
<li>U+27FC LONG RIGHTWARDS ARROW FROM BAR: try adding math</li>
<li>U+27FD LONG LEFTWARDS DOUBLE ARROW FROM BAR: try adding math</li>
<li>U+27FE LONG RIGHTWARDS DOUBLE ARROW FROM BAR: try adding math</li>
<li>U+27FF LONG RIGHTWARDS SQUIGGLE ARROW: try adding math</li>
<li>U+2E17 DOUBLE OBLIQUE HYPHEN: try adding coptic</li>
</ul>
<p>Or you can add the above codepoints to one of the subsets supported by the font: <code>cyrillic</code>, <code>cyrillic-ext</code>, <code>greek</code>, <code>greek-ext</code>, <code>latin</code>, <code>latin-ext</code>, <code>vietnamese</code></p>
 [code: unreachable-subsetting]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Are there any misaligned on-curve points? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#outline-alignment-miss">outline_alignment_miss</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have on-curve points which have potentially incorrect y coordinates:</p>
<pre><code>* uni2147 (U+2147): X=761.0,Y=1.0 (should be at baseline 0?)

* uni220C (U+220C): X=463.0,Y=1.0 (should be at baseline 0?)

* uni2270 (U+2270): X=1076.0,Y=1478.0 (should be at cap-height 1480?)

* uni22EC (U+22EC): X=1076.0,Y=1478.0 (should be at cap-height 1480?)
</code></pre>
 [code: found-misalignments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Do outlines contain any jaggy segments? <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/universal.html#outline-jaggy-segments">outline_jaggy_segments</a></summary>
    <div>







* ⚠️ **WARN** <p>The following glyphs have jaggy segments:</p>
<pre><code>* ordfeminine.cv23: L&lt;&lt;548.0,1607.0&gt;--&lt;548.0,1540.0&gt;&gt;/B&lt;&lt;548.0,1540.0&gt;-&lt;541.0,1569.0&gt;-&lt;498.0,1619.0&gt;-&lt;399.0,1619.0&gt;&gt; = 13.570434385161475

* phi.sc: B&lt;&lt;1150.0,600.0&gt;-&lt;1150.0,750.0&gt;-&lt;1046.0,895.0&gt;-&lt;781.0,940.0&gt;&gt;/L&lt;&lt;781.0,940.0&gt;--&lt;940.0,940.0&gt;&gt; = 9.637538112930923

* phi.sc: B&lt;&lt;50.0,600.0&gt;-&lt;50.0,450.0&gt;-&lt;154.0,305.0&gt;-&lt;419.0,260.0&gt;&gt;/L&lt;&lt;419.0,260.0&gt;--&lt;260.0,260.0&gt;&gt; = 9.637538112930923

* phi.sc: L&lt;&lt;260.0,940.0&gt;--&lt;419.0,940.0&gt;&gt;/B&lt;&lt;419.0,940.0&gt;-&lt;154.0,895.0&gt;-&lt;50.0,750.0&gt;-&lt;50.0,600.0&gt;&gt; = 9.637538112930923

* phi.sc: L&lt;&lt;940.0,260.0&gt;--&lt;781.0,260.0&gt;&gt;/B&lt;&lt;781.0,260.0&gt;-&lt;1046.0,305.0&gt;-&lt;1150.0,450.0&gt;-&lt;1150.0,600.0&gt;&gt; = 9.637538112930923

* uni01DB (U+01DB): L&lt;&lt;349.0,2076.0&gt;--&lt;547.0,1851.0&gt;&gt;/B&lt;&lt;547.0,1851.0&gt;-&lt;514.0,1877.0&gt;-&lt;472.0,1892.0&gt;-&lt;426.0,1892.0&gt;&gt; = 10.418397602859336

* uni01DC (U+01DC): L&lt;&lt;204.0,1736.0&gt;--&lt;402.0,1511.0&gt;&gt;/B&lt;&lt;402.0,1511.0&gt;-&lt;369.0,1537.0&gt;-&lt;327.0,1552.0&gt;-&lt;281.0,1552.0&gt;&gt; = 10.418397602859336

* uni01DC.cv25: L&lt;&lt;204.0,1736.0&gt;--&lt;402.0,1511.0&gt;&gt;/B&lt;&lt;402.0,1511.0&gt;-&lt;369.0,1537.0&gt;-&lt;327.0,1552.0&gt;-&lt;281.0,1552.0&gt;&gt; = 10.418397602859336

* uni01DC.sc: L&lt;&lt;253.0,1896.0&gt;--&lt;451.0,1671.0&gt;&gt;/B&lt;&lt;451.0,1671.0&gt;-&lt;418.0,1697.0&gt;-&lt;376.0,1712.0&gt;-&lt;330.0,1712.0&gt;&gt; = 10.418397602859336

* uni01E4.cv21: L&lt;&lt;870.0,316.0&gt;--&lt;906.0,316.0&gt;&gt;/B&lt;&lt;906.0,316.0&gt;-&lt;876.0,309.0&gt;-&lt;844.0,306.0&gt;-&lt;810.0,306.0&gt;&gt; = 13.134022306396327

* uni01E5.cv24: B&lt;&lt;810.0,100.0&gt;-&lt;815.0,108.0&gt;-&lt;819.0,115.0&gt;-&lt;820.0,120.0&gt;&gt;/L&lt;&lt;820.0,120.0&gt;--&lt;820.0,100.0&gt;&gt; = 11.309932474020195

* uni0308_gravecomb: L&lt;&lt;158.0,1736.0&gt;--&lt;356.0,1511.0&gt;&gt;/B&lt;&lt;356.0,1511.0&gt;-&lt;323.0,1537.0&gt;-&lt;281.0,1552.0&gt;-&lt;235.0,1552.0&gt;&gt; = 10.418397602859336

* uni1D43.cv23: L&lt;&lt;548.0,1413.0&gt;--&lt;548.0,1346.0&gt;&gt;/B&lt;&lt;548.0,1346.0&gt;-&lt;541.0,1375.0&gt;-&lt;498.0,1425.0&gt;-&lt;399.0,1425.0&gt;&gt; = 13.570434385161475

* uni1FD2 (U+1FD2): L&lt;&lt;-142.0,1736.0&gt;--&lt;56.0,1511.0&gt;&gt;/B&lt;&lt;56.0,1511.0&gt;-&lt;23.0,1537.0&gt;-&lt;-19.0,1552.0&gt;-&lt;-65.0,1552.0&gt;&gt; = 10.418397602859336

* uni1FD2.sc.cv22: L&lt;&lt;-140.0,1896.0&gt;--&lt;58.0,1671.0&gt;&gt;/B&lt;&lt;58.0,1671.0&gt;-&lt;25.0,1697.0&gt;-&lt;-17.0,1712.0&gt;-&lt;-63.0,1712.0&gt;&gt; = 10.418397602859336

* uni1FD2.sc: L&lt;&lt;19.0,1896.0&gt;--&lt;217.0,1671.0&gt;&gt;/B&lt;&lt;217.0,1671.0&gt;-&lt;184.0,1697.0&gt;-&lt;142.0,1712.0&gt;-&lt;96.0,1712.0&gt;&gt; = 10.418397602859336

* uni1FE2 (U+1FE2): L&lt;&lt;144.0,1736.0&gt;--&lt;342.0,1511.0&gt;&gt;/B&lt;&lt;342.0,1511.0&gt;-&lt;309.0,1537.0&gt;-&lt;267.0,1552.0&gt;-&lt;221.0,1552.0&gt;&gt; = 10.418397602859336

* uni1FE2.sc: L&lt;&lt;287.0,1896.0&gt;--&lt;485.0,1671.0&gt;&gt;/B&lt;&lt;485.0,1671.0&gt;-&lt;452.0,1697.0&gt;-&lt;410.0,1712.0&gt;-&lt;364.0,1712.0&gt;&gt; = 10.418397602859336

* uni1FED (U+1FED): L&lt;&lt;158.0,1736.0&gt;--&lt;356.0,1511.0&gt;&gt;/B&lt;&lt;356.0,1511.0&gt;-&lt;323.0,1537.0&gt;-&lt;281.0,1552.0&gt;-&lt;235.0,1552.0&gt;&gt; = 10.418397602859336

* uni2090.cv23: L&lt;&lt;500.0,421.0&gt;--&lt;500.0,354.0&gt;&gt;/B&lt;&lt;500.0,354.0&gt;-&lt;493.0,383.0&gt;-&lt;450.0,433.0&gt;-&lt;351.0,433.0&gt;&gt; = 13.570434385161475

* uni209A (U+209A): L&lt;&lt;340.0,-442.0&gt;--&lt;340.0,-126.0&gt;&gt;/B&lt;&lt;340.0,-126.0&gt;-&lt;347.0,-155.0&gt;-&lt;390.0,-206.0&gt;-&lt;489.0,-206.0&gt;&gt; = 13.570434385161475

* uni2100.cv23: L&lt;&lt;534.0,1392.0&gt;--&lt;534.0,1325.0&gt;&gt;/B&lt;&lt;534.0,1325.0&gt;-&lt;527.0,1354.0&gt;-&lt;484.0,1404.0&gt;-&lt;385.0,1404.0&gt;&gt; = 13.570434385161475

* uni2101.cv23: L&lt;&lt;534.0,1392.0&gt;--&lt;534.0,1325.0&gt;&gt;/B&lt;&lt;534.0,1325.0&gt;-&lt;527.0,1354.0&gt;-&lt;484.0,1404.0&gt;-&lt;385.0,1404.0&gt;&gt; = 13.570434385161475

* uni2104 (U+2104): B&lt;&lt;410.0,900.0&gt;-&lt;410.0,934.0&gt;-&lt;413.0,964.0&gt;-&lt;420.0,992.0&gt;&gt;/L&lt;&lt;420.0,992.0&gt;--&lt;420.0,809.0&gt;&gt; = 14.036243467926484

* uni210A (U+210A): B&lt;&lt;379.0,397.0&gt;-&lt;397.0,417.0&gt;-&lt;418.0,440.0&gt;-&lt;441.0,468.0&gt;&gt;/B&lt;&lt;441.0,468.0&gt;-&lt;379.0,380.0&gt;-&lt;348.0,299.0&gt;-&lt;348.0,224.0&gt;&gt; = 4.23422462768641

* uni210A (U+210A): B&lt;&lt;733.0,59.0&gt;-&lt;758.0,80.0&gt;-&lt;776.0,98.0&gt;-&lt;787.0,110.0&gt;&gt;/L&lt;&lt;787.0,110.0&gt;--&lt;717.0,-11.0&gt;&gt; = 12.460533457013435

* uni210B (U+210B): B&lt;&lt;1077.0,1099.0&gt;-&lt;1118.0,1132.0&gt;-&lt;1155.0,1165.0&gt;-&lt;1188.0,1195.0&gt;&gt;/B&lt;&lt;1188.0,1195.0&gt;-&lt;1101.0,1089.0&gt;-&lt;1030.0,986.0&gt;-&lt;975.0,888.0&gt;&gt; = 8.34871162099596

* uni2133 (U+2133): B&lt;&lt;2219.0,1344.0&gt;-&lt;2278.0,1392.0&gt;-&lt;2318.0,1423.0&gt;-&lt;2340.0,1438.0&gt;&gt;/B&lt;&lt;2340.0,1438.0&gt;-&lt;2332.0,1430.0&gt;-&lt;2315.0,1412.0&gt;-&lt;2291.0,1384.0&gt;&gt; = 10.713123022791033

* uni22D6 (U+22D6): B&lt;&lt;1018.0,860.0&gt;-&lt;1000.0,860.0&gt;-&lt;982.0,858.0&gt;-&lt;966.0,853.0&gt;&gt;/L&lt;&lt;966.0,853.0&gt;--&lt;1162.0,930.0&gt;&gt; = 4.093711690843978

* uni22D6 (U+22D6): B&lt;&lt;818.0,660.0&gt;-&lt;818.0,583.0&gt;-&lt;861.0,516.0&gt;-&lt;925.0,483.0&gt;&gt;/L&lt;&lt;925.0,483.0&gt;--&lt;472.0,660.0&gt;&gt; = 5.934760381876358

* uni22D6 (U+22D6): L&lt;&lt;1162.0,390.0&gt;--&lt;965.0,467.0&gt;&gt;/B&lt;&lt;965.0,467.0&gt;-&lt;982.0,462.0&gt;-&lt;1000.0,460.0&gt;-&lt;1018.0,460.0&gt;&gt; = 4.9591463393229605

* uni22D6 (U+22D6): L&lt;&lt;472.0,660.0&gt;--&lt;924.0,837.0&gt;&gt;/B&lt;&lt;924.0,837.0&gt;-&lt;861.0,804.0&gt;-&lt;818.0,737.0&gt;-&lt;818.0,660.0&gt;&gt; = 6.26101600748654

* uni2469.cv01.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv01.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2469.cv01.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv01.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2469.cv11.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv11.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2469.cv11.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv11.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2469.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2469.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2469.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2473.cv02.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2473.cv02.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2473.cv12.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2473.cv12.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni2473.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni2473.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni247D.cv01.cv20.ss06.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv01.cv20.ss06.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni247D.cv01.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv01.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni247D.cv11.cv20.ss06.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv11.cv20.ss06.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni247D.cv11.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv11.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni247D.cv20.ss06.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv20.ss06.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni247D.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni247D.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni2487.cv02.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni2487.cv02.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni2487.cv12.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni2487.cv12.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni2487.cv20.zero: L&lt;&lt;1731.0,306.0&gt;--&lt;1877.0,941.0&gt;&gt;/L&lt;&lt;1877.0,941.0&gt;--&lt;1877.0,940.0&gt;&gt; = 12.94847962754237

* uni2487.cv20.zero: L&lt;&lt;1734.0,1172.0&gt;--&lt;1589.0,537.0&gt;&gt;/L&lt;&lt;1589.0,537.0&gt;--&lt;1589.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv01.cv20.ss06.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv01.cv20.ss06.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv01.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv01.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv11.cv20.ss06.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv11.cv20.ss06.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv11.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv11.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv20.ss06.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv20.ss06.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni2491.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni2491.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni249B.cv02.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni249B.cv02.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni249B.cv12.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni249B.cv12.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni249B.cv20.zero: L&lt;&lt;1234.0,306.0&gt;--&lt;1380.0,941.0&gt;&gt;/L&lt;&lt;1380.0,941.0&gt;--&lt;1380.0,940.0&gt;&gt; = 12.94847962754237

* uni249B.cv20.zero: L&lt;&lt;1237.0,1172.0&gt;--&lt;1092.0,537.0&gt;&gt;/L&lt;&lt;1092.0,537.0&gt;--&lt;1092.0,540.0&gt;&gt; = 12.86275101895821

* uni24D0.cv23: L&lt;&lt;923.0,1047.0&gt;--&lt;923.0,980.0&gt;&gt;/B&lt;&lt;923.0,980.0&gt;-&lt;916.0,1009.0&gt;-&lt;873.0,1059.0&gt;-&lt;774.0,1059.0&gt;&gt; = 13.570434385161475

* uni24D1 (U+24D1): B&lt;&lt;939.0,932.0&gt;-&lt;840.0,932.0&gt;-&lt;797.0,882.0&gt;-&lt;790.0,853.0&gt;&gt;/L&lt;&lt;790.0,853.0&gt;--&lt;790.0,1169.0&gt;&gt; = 13.570434385161475

* uni24D3 (U+24D3): L&lt;&lt;923.0,1169.0&gt;--&lt;923.0,853.0&gt;&gt;/B&lt;&lt;923.0,853.0&gt;-&lt;916.0,882.0&gt;-&lt;873.0,932.0&gt;-&lt;774.0,932.0&gt;&gt; = 13.570434385161475

* uni24D6.cv24: L&lt;&lt;933.0,1047.0&gt;--&lt;933.0,980.0&gt;&gt;/B&lt;&lt;933.0,980.0&gt;-&lt;926.0,1009.0&gt;-&lt;883.0,1059.0&gt;-&lt;784.0,1059.0&gt;&gt; = 13.570434385161475

* uni24DF (U+24DF): L&lt;&lt;790.0,185.0&gt;--&lt;790.0,501.0&gt;&gt;/B&lt;&lt;790.0,501.0&gt;-&lt;797.0,472.0&gt;-&lt;840.0,421.0&gt;-&lt;939.0,421.0&gt;&gt; = 13.570434385161475

* uni24E8 (U+24E8): B&lt;&lt;860.0,100.0&gt;-&lt;731.0,100.0&gt;-&lt;613.0,136.0&gt;-&lt;514.0,198.0&gt;&gt;/B&lt;&lt;514.0,198.0&gt;-&lt;546.0,182.0&gt;-&lt;591.0,166.0&gt;-&lt;651.0,166.0&gt;&gt; = 5.4923245571273185

* uni24F4.cv02.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni24F4.cv02.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni24F4.cv02.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni24F4.cv02.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni24F4.cv12.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni24F4.cv12.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni24F4.cv12.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni24F4.cv12.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni24F4.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni24F4.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni24F4.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni24F4.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni24FE.cv01.cv10.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10.ss06.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10.ss06: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv10: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv01.cv10: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv01.cv20.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.ss06.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv01.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv01.cv20.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.ss06: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv01.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv01.cv20: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv01.cv20: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv01.cv20: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv10.cv11.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11.ss06.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11.ss06.zero: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv10.cv11.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11.ss06: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11.ss06: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv10.cv11.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.cv11: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.cv11: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.ss06.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.ss06: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10.zero: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10: B&lt;&lt;1109.0,294.0&gt;-&lt;1154.0,294.0&gt;-&lt;1195.0,306.0&gt;-&lt;1230.0,331.0&gt;&gt;/B&lt;&lt;1230.0,331.0&gt;-&lt;1135.0,246.0&gt;-&lt;1007.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 6.282492088161278

* uni24FE.cv10: B&lt;&lt;1375.0,740.0&gt;-&lt;1375.0,878.0&gt;-&lt;1350.0,986.0&gt;-&lt;1308.0,1061.0&gt;&gt;/B&lt;&lt;1308.0,1061.0&gt;-&lt;1369.0,973.0&gt;-&lt;1404.0,863.0&gt;-&lt;1404.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,617.0&gt;-&lt;1369.0,507.0&gt;-&lt;1308.0,419.0&gt;&gt;/B&lt;&lt;1308.0,419.0&gt;-&lt;1350.0,494.0&gt;-&lt;1375.0,602.0&gt;-&lt;1375.0,740.0&gt;&gt; = 5.480169942973905

* uni24FE.cv10: B&lt;&lt;860.0,1284.0&gt;-&lt;1007.0,1284.0&gt;-&lt;1135.0,1234.0&gt;-&lt;1230.0,1149.0&gt;&gt;/B&lt;&lt;1230.0,1149.0&gt;-&lt;1195.0,1174.0&gt;-&lt;1154.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 6.282492088161278

* uni24FE.cv11.cv20.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.ss06.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv11.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv11.cv20.ss06.zero: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv11.cv20.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.ss06: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.ss06: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv11.cv20.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv11.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv11.cv20: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.cv20: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv11.cv20: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv11.ss06.zero: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv11.ss06: L&lt;&lt;524.0,1169.0&gt;--&lt;433.0,1089.0&gt;&gt;/B&lt;&lt;433.0,1089.0&gt;-&lt;530.0,1210.0&gt;-&lt;681.0,1284.0&gt;-&lt;860.0,1284.0&gt;&gt; = 9.963114261191809

* uni24FE.cv20.ss06.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.ss06.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.ss06.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.ss06.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.ss06.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv20.ss06.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv20.ss06: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.ss06: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.ss06: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.ss06: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.zero: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.zero: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.zero: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20.zero: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20.zero: L&lt;&lt;1107.0,533.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1180.0,644.0&gt;&gt; = 13.250821205891214

* uni24FE.cv20.zero: L&lt;&lt;1111.0,945.0&gt;--&lt;1039.0,638.0&gt;&gt;/L&lt;&lt;1039.0,638.0&gt;--&lt;1039.0,835.0&gt;&gt; = 13.198903231376033

* uni24FE.cv20: B&lt;&lt;1109.0,294.0&gt;-&lt;1159.0,294.0&gt;-&lt;1203.0,310.0&gt;-&lt;1239.0,339.0&gt;&gt;/B&lt;&lt;1239.0,339.0&gt;-&lt;1143.0,249.0&gt;-&lt;1012.0,196.0&gt;-&lt;860.0,196.0&gt;&gt; = 4.2990153936520965

* uni24FE.cv20: B&lt;&lt;1351.0,856.0&gt;-&lt;1351.0,949.0&gt;-&lt;1328.0,1030.0&gt;-&lt;1288.0,1088.0&gt;&gt;/B&lt;&lt;1288.0,1088.0&gt;-&lt;1361.0,996.0&gt;-&lt;1404.0,876.0&gt;-&lt;1404.0,740.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20: B&lt;&lt;1404.0,740.0&gt;-&lt;1404.0,604.0&gt;-&lt;1361.0,484.0&gt;-&lt;1288.0,392.0&gt;&gt;/B&lt;&lt;1288.0,392.0&gt;-&lt;1328.0,450.0&gt;-&lt;1351.0,531.0&gt;-&lt;1351.0,624.0&gt;&gt; = 3.838947190668937

* uni24FE.cv20: B&lt;&lt;860.0,1284.0&gt;-&lt;1012.0,1284.0&gt;-&lt;1143.0,1231.0&gt;-&lt;1239.0,1141.0&gt;&gt;/B&lt;&lt;1239.0,1141.0&gt;-&lt;1203.0,1170.0&gt;-&lt;1159.0,1186.0&gt;-&lt;1109.0,1186.0&gt;&gt; = 4.2990153936520965

* uni277F.cv01.cv20.ss06.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv01.cv20.ss06.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.cv01.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv01.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.cv01.ss06.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.cv01.ss06.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni277F.cv01.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.cv01.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni277F.cv11.cv20.ss06.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv11.cv20.ss06.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.cv11.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv11.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.cv11.ss06.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.cv11.ss06.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni277F.cv11.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.cv11.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni277F.cv20.ss06.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv20.ss06.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.cv20.zero: L&lt;&lt;1038.0,835.0&gt;--&lt;1038.0,638.0&gt;&gt;/L&lt;&lt;1038.0,638.0&gt;--&lt;1111.0,945.0&gt;&gt; = 13.375675740284615

* uni277F.cv20.zero: L&lt;&lt;1180.0,644.0&gt;--&lt;1180.0,843.0&gt;&gt;/L&lt;&lt;1180.0,843.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.250821205891214

* uni277F.ss06.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.ss06.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597

* uni277F.zero: L&lt;&lt;1048.0,740.0&gt;--&lt;1048.0,681.0&gt;&gt;/L&lt;&lt;1048.0,681.0&gt;--&lt;1111.0,947.0&gt;&gt; = 13.324531261890783

* uni277F.zero: L&lt;&lt;1170.0,740.0&gt;--&lt;1170.0,800.0&gt;&gt;/L&lt;&lt;1170.0,800.0&gt;--&lt;1107.0,533.0&gt;&gt; = 13.27639704231597
</code></pre>
 [code: found-jaggy-segments]



</div>
</details>

<details>
    <summary>⚠️ <b>WARN</b> Checking OS/2 achVendID. <a href="https://fontbakery.readthedocs.io/en/stable/fontbakery/checks/googlefonts.html#googlefonts-vendor-id">googlefonts/vendor_id</a></summary>
    <div>







* ⚠️ **WARN** <p>OS/2 VendorID is 'PfEd', a font editor default. If you registered it recently, then it's safe to ignore this warning message. Otherwise, you should set it to your own unique 4 character code, and register it with Microsoft at <a href="https://www.microsoft.com/typography/links/vendorlist.aspx">https://www.microsoft.com/typography/links/vendorlist.aspx</a></p>
 [code: bad]



</div>
</details>
</div>
</details>




### Summary

| 💥 ERROR | ☠ FATAL | 🔥 FAIL | ⚠️ WARN | ⏩ SKIP | ℹ️ INFO | ✅ PASS | 🔎 DEBUG | 
| ---|---|---|---|---|---|---|---|
| 2 | 0 | 3 | 16 | 234 | 11 | 189 | 0 | 
| 0% | 0% | 1% | 4% | 51% | 2% | 42% | 0% | 



**Note:** The following loglevels were omitted in this report:


* SKIP
* INFO
* PASS
* DEBUG
