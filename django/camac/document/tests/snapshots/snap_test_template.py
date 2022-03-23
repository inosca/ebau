# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_template_download[Municipality-template__path0] 1'] = '''<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:spacing w:before="200" w:after="120"/>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Camac Vorlage – Beispiele</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Einzelne Werte</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Dossier: {{ identifier }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:sz w:val="21"/>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Gemeinde: {{ location }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Art der befestigten Fläche: {{ field_art_der_befestigten_flache }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Publikationsdatum: {{ publication_date }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Standort Eingaben:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ field_ortsbezeichnung_des_vorhabens }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ field_standort_adresse }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ field_standort_</w:t>
    </w:r>
    <w:r>
      <w:rPr/>
      <w:t xml:space="preserve">spezialbezeichnung </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>}}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ field_standort_ort }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Listen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="TextBody"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Kategorie des Vorhabens:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{%p for kategorie in field_kategorie_des_vorhabens %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:numPr>
        <w:ilvl w:val="0"/>
        <w:numId w:val="3"/>
      </w:numPr>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ kategorie }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{%p endfor %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Publikation:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">{%p for </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>publikation</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"> in </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>publications</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"> %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:numPr>
        <w:ilvl w:val="0"/>
        <w:numId w:val="3"/>
      </w:numPr>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">{{ </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>publikation.calendar_week</w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"> }} {{ </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">publikation.date </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>}}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{%p endfor %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>{{ field_publikation_bemerkung }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Tabellen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Grundeigentümerschaft</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr for grundeigentumerschaft in field_grundeigentumerschaft %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:bookmarkStart w:id="0" w:name="__DdeLink__836_1620457326"/>
          <w:bookmarkEnd w:id="0"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.firma }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.name }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.strasse }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.ort }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.email }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ grundeigentumerschaft.tel }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Bauherrschaft</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr for bauherrschaft in field_bauherrschaft %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.firma }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.name }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.strasse }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.ort }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.email }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ bauherrschaft.tel }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Projekt Verfasser / Planer</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr for projektverfasser_planer in field_projektverfasser_planer %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.firma }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.name }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.strasse }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.ort }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.email }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ projektverfasser_planer.tel }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Gebühren</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="2422"/>
      <w:gridCol w:w="2698"/>
      <w:gridCol w:w="1720"/>
      <w:gridCol w:w="1351"/>
      <w:gridCol w:w="1447"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2422" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Leistung</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2698" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1720" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Konto</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1351" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Betrag</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1447" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Erfasst am</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9638" w:type="dxa"/>
          <w:gridSpan w:val="5"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{%tr for </w:t>
          </w:r>
          <w:bookmarkStart w:id="1" w:name="__DdeLink__223_939317217"/>
          <w:bookmarkStart w:id="2" w:name="__DdeLink__431_6905944341"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="2"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry</w:t>
          </w:r>
          <w:bookmarkEnd w:id="1"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"> in billing_entries %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2422" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:bookmarkStart w:id="3" w:name="__DdeLink__431_69059443411"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="3"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry.account }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2698" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:bookmarkStart w:id="4" w:name="__DdeLink__431_69059443412"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="4"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry.service }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1720" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:bookmarkStart w:id="5" w:name="__DdeLink__431_690594434121"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="5"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry.account_number }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1351" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:bookmarkStart w:id="6" w:name="__DdeLink__431_690594434122"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="6"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry.amount }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1447" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:bookmarkStart w:id="7" w:name="__DdeLink__431_690594434123"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>b</w:t>
          </w:r>
          <w:bookmarkEnd w:id="7"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>illing_entry.created }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9638" w:type="dxa"/>
          <w:gridSpan w:val="5"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Zirkulation</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1134"/>
      <w:gridCol w:w="1981"/>
      <w:gridCol w:w="964"/>
      <w:gridCol w:w="1023"/>
      <w:gridCol w:w="1359"/>
      <w:gridCol w:w="1595"/>
      <w:gridCol w:w="1581"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Zustellungsgrund</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="964" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Frist</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1023" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Status</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Start</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Ende</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Antwort</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{%tr for </w:t>
          </w:r>
          <w:bookmarkStart w:id="8" w:name="__DdeLink__431_69059443413"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>a</w:t>
          </w:r>
          <w:bookmarkEnd w:id="8"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>ctivation in activations %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.service }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.reason }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="964" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.deadline_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1023" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.circulation_state }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.start_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.end_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.circulation_answer }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Zirkulation</w:t>
    </w:r>
    <w:r>
      <w:rPr/>
      <w:t xml:space="preserve"> gefiltert nach </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Antwort</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1134"/>
      <w:gridCol w:w="1981"/>
      <w:gridCol w:w="963"/>
      <w:gridCol w:w="1024"/>
      <w:gridCol w:w="1359"/>
      <w:gridCol w:w="1595"/>
      <w:gridCol w:w="1581"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Zustellungsgrund</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="963" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Frist</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1024" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Status</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Start</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Ende</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Antwort</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">{%tr for </w:t>
          </w:r>
          <w:bookmarkStart w:id="9" w:name="__DdeLink__431_690594434131"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>a</w:t>
          </w:r>
          <w:bookmarkEnd w:id="9"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>ctivation in activations %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr if activation.circulation_answer == "Fachbereich nicht betroffen / keine Bemerkungen" %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.service }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.reason }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="963" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.deadline_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1024" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.circulation_state }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.start_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.end_date }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{{ activation.circulation_answer }}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endif %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9637" w:type="dxa"/>
          <w:gridSpan w:val="7"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Einsprachen</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9643" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="55" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="55" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1606"/>
      <w:gridCol w:w="1606"/>
      <w:gridCol w:w="1607"/>
      <w:gridCol w:w="1606"/>
      <w:gridCol w:w="1675"/>
      <w:gridCol w:w="1543"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9643" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>{%tr for objection in objections %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>Datum</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="3213" w:type="dxa"/>
          <w:gridSpan w:val="2"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>{{ o</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">bjection.creation_date </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>Titel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="3218" w:type="dxa"/>
          <w:gridSpan w:val="2"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>{{ o</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>bjection.</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>title }}</w:t>
          </w:r>
        </w:p>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>Name</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1607" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:rFonts w:ascii="Liberation Serif" w:hAnsi="Liberation Serif" w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:b/>
              <w:b/>
              <w:bCs/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:b/>
              <w:bCs/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:rFonts w:ascii="Liberation Serif" w:hAnsi="Liberation Serif" w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:b/>
              <w:b/>
              <w:bCs/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:b/>
              <w:bCs/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1675" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1543" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr>
              <w:b/>
              <w:b/>
              <w:bCs/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:b/>
              <w:bCs/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9643" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{%tr for </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>participant</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve"> in objection.</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>participants</w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve"> %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.company </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.name </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1607" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.address </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1606" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.city </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1675" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.email </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1543" w:type="dxa"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">{{ </w:t>
          </w:r>
          <w:r>
            <w:rPr>
              <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
              <w:color w:val="00000A"/>
              <w:kern w:val="0"/>
              <w:sz w:val="24"/>
              <w:szCs w:val="24"/>
              <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">participant.phone </w:t>
          </w:r>
          <w:r>
            <w:rPr/>
            <w:t>}}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9643" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="9643" w:type="dxa"/>
          <w:gridSpan w:val="6"/>
          <w:tcBorders>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000000"/>
          </w:tcBorders>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:keepNext w:val="true"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>{%tr endfor %}</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Stellungsnahmen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{%p for activation in activations %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t>Bericht von {{ activation.service }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{%p for notice in activation.notices %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t>{{ notice.notice_type }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{{ notice.content }}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{%p endfor %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{%p endfor %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:spacing w:before="240" w:after="120"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Stellungsnahmen der Aktuellen Fachstelle</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>{%p for activation in my_activations %}</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t>Bericht von {{ activation.service }}</w:t>
      <w:br/>
    </w:r>
    <w:r>
      <w:rPr/>
      <w:t>{%p endfor %}</w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
'''

snapshots['test_template_merge[testname-11-18-011-Schwyz-activation__service0-instance__group0-Grund-OK-Antwort-Amt-Allgemein-Gebuehren-Canton-template__path0-instance__user0-200-docx-99.66-activation__deadline_date0-activation__end_date0-activation__start_date0-billing_entry__created0-publication_entry__publication_date0] 1'] = '''<w:body xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w10="urn:schemas-microsoft-com:office:word" xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml">
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:spacing w:before="200" w:after="120"/>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Camac Vorlage – Beispiele</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Einzelne Werte</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Dossier: 11-18-011</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:sz w:val="21"/>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Gemeinde: Schwyz</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Art der befestigten Fläche: Lagerplatz</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Publikationsdatum: 28.05.2018</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Standort Eingaben:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Listen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="TextBody"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Kategorie des Vorhabens:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:numPr>
        <w:ilvl w:val="0"/>
        <w:numId w:val="3"/>
      </w:numPr>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Anlage(n)</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:numPr>
        <w:ilvl w:val="0"/>
        <w:numId w:val="3"/>
      </w:numPr>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Baute(n)</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve">Publikation:</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:lang w:val="de-CH"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:sz w:val="24"/>
        <w:szCs w:val="24"/>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t xml:space="preserve"/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading2"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:ind w:left="0" w:hanging="0"/>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Tabellen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:numPr>
        <w:ilvl w:val="1"/>
        <w:numId w:val="2"/>
      </w:numPr>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Grundeigentümerschaft</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:bookmarkStart w:id="0" w:name="__DdeLink__836_1620457326"/>
          <w:bookmarkEnd w:id="0"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Beispiel Strasse</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">0000 Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">email@example.com</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">000 000 00 00</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:bookmarkStart w:id="0" w:name="__DdeLink__836_1620457326"/>
          <w:bookmarkEnd w:id="0"/>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Bauherrschaft</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Beispiel Strasse</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">0000 Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">email@example.com</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">000 000 00 00</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Projekt Verfasser / Planer</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1011"/>
      <w:gridCol w:w="1864"/>
      <w:gridCol w:w="1442"/>
      <w:gridCol w:w="1806"/>
      <w:gridCol w:w="1890"/>
      <w:gridCol w:w="1624"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Firma</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Name, Vorname</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Strasse, Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>PLZ, Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>E-Mail</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Tel. Nr.</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Muster</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Beispiel Strasse</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">0000 Ort</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">email@example.com</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">000 000 00 00</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1011" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Firma Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1864" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Hans Beispiel</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1442" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1806" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1890" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1624" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve"/>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Gebühren</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="2422"/>
      <w:gridCol w:w="2698"/>
      <w:gridCol w:w="1720"/>
      <w:gridCol w:w="1351"/>
      <w:gridCol w:w="1447"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2422" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Leistung</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2698" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1720" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Konto</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1351" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Betrag</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1447" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Erfasst am</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2422" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Allgemein / Gebuehren</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="2698" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Amt</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1720" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">0000</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1351" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">99.66</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1447" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">28.05.2018</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Zirkulation</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1134"/>
      <w:gridCol w:w="1981"/>
      <w:gridCol w:w="964"/>
      <w:gridCol w:w="1023"/>
      <w:gridCol w:w="1359"/>
      <w:gridCol w:w="1595"/>
      <w:gridCol w:w="1581"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Zustellungsgrund</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="964" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Frist</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1023" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Status</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Start</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Ende</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">Antwort</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Grund</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="964" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">30.04.2018</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1023" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">OK</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">15.03.2018</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">15.04.2018</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableContents"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t xml:space="preserve">Antwort</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Zirkulation</w:t>
    </w:r>
    <w:r>
      <w:rPr/>
      <w:t xml:space="preserve"> gefiltert nach </w:t>
    </w:r>
    <w:r>
      <w:rPr>
        <w:rFonts w:eastAsia="Noto Sans CJK SC Regular" w:cs="FreeSans"/>
        <w:color w:val="00000A"/>
        <w:kern w:val="0"/>
        <w:sz w:val="28"/>
        <w:szCs w:val="28"/>
        <w:lang w:val="en-US" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
      </w:rPr>
      <w:t>Antwort</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9638" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="47" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="40" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid>
      <w:gridCol w:w="1134"/>
      <w:gridCol w:w="1981"/>
      <w:gridCol w:w="963"/>
      <w:gridCol w:w="1024"/>
      <w:gridCol w:w="1359"/>
      <w:gridCol w:w="1595"/>
      <w:gridCol w:w="1581"/>
    </w:tblGrid>
    <w:tr>
      <w:trPr/>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1134" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Fachstelle</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1981" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Zustellungsgrund</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="963" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Frist</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1024" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Status</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1359" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr>
              <w:lang w:val="de-CH" w:eastAsia="zh-CN" w:bidi="hi-IN"/>
            </w:rPr>
            <w:t>Start</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1595" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t>Ende</w:t>
          </w:r>
        </w:p>
      </w:tc>
      <w:tc>
        <w:tcPr>
          <w:tcW w:w="1581" w:type="dxa"/>
          <w:tcBorders>
            <w:top w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:left w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:bottom w:val="single" w:sz="2" w:space="0" w:color="000001"/>
            <w:right w:val="single" w:sz="2" w:space="0" w:color="000001"/>
          </w:tcBorders>
          <w:shd w:fill="auto" w:val="clear"/>
        </w:tcPr>
        <w:p>
          <w:pPr>
            <w:pStyle w:val="TableHeading"/>
            <w:widowControl w:val="false"/>
            <w:rPr/>
          </w:pPr>
          <w:r>
            <w:rPr/>
            <w:t xml:space="preserve">Antwort</w:t>
          </w:r>
        </w:p>
      </w:tc>
    </w:tr>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Einsprachen</w:t>
    </w:r>
  </w:p>
  <w:tbl>
    <w:tblPr>
      <w:tblW w:w="9643" w:type="dxa"/>
      <w:jc w:val="left"/>
      <w:tblInd w:w="55" w:type="dxa"/>
      <w:tblLayout w:type="fixed"/>
      <w:tblCellMar>
        <w:top w:w="55" w:type="dxa"/>
        <w:left w:w="55" w:type="dxa"/>
        <w:bottom w:w="55" w:type="dxa"/>
        <w:right w:w="55" w:type="dxa"/>
      </w:tblCellMar>
    </w:tblPr>
    <w:tblGrid/>
  </w:tbl>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Stellungsnahmen</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t xml:space="preserve">Bericht von Fachstelle</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t xml:space="preserve">Antrag</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t xml:space="preserve">Inhalt Antrag!</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr>
        <w:b/>
        <w:b/>
        <w:bCs/>
      </w:rPr>
    </w:pPr>
    <w:r>
      <w:rPr>
        <w:b/>
        <w:bCs/>
      </w:rPr>
      <w:t xml:space="preserve">Hinweis</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Normal"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t xml:space="preserve">Inhalt Hinweis!</w:t>
    </w:r>
  </w:p>
  <w:p>
    <w:pPr>
      <w:pStyle w:val="Heading3"/>
      <w:spacing w:before="240" w:after="120"/>
      <w:rPr/>
    </w:pPr>
    <w:r>
      <w:rPr/>
      <w:t>Stellungsnahmen der Aktuellen Fachstelle</w:t>
    </w:r>
  </w:p>
  <w:sectPr>
    <w:type w:val="nextPage"/>
    <w:pgSz w:w="11906" w:h="16838"/>
    <w:pgMar w:left="1134" w:right="1134" w:header="0" w:top="1134" w:footer="0" w:bottom="1134" w:gutter="0"/>
    <w:pgNumType w:fmt="decimal"/>
    <w:formProt w:val="false"/>
    <w:textDirection w:val="lrTb"/>
    <w:docGrid w:type="default" w:linePitch="240" w:charSpace="0"/>
  </w:sectPr>
</w:body>
'''
