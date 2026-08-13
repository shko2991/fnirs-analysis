#!/usr/bin/env python3
import os, math, random, textwrap, zipfile, datetime, html, base64, tarfile
from pathlib import Path
ROOT=Path(__file__).parent
OUT=ROOT/'deliverables'; AS=OUT/'assets'; OUT.mkdir(exist_ok=True); AS.mkdir(exist_ok=True)
W,H=1600,900
navy='#0B1736'; ink='#14213D'; blue='#3366FF'; cyan='#21C4D6'; violet='#8257E5'; coral='#FF6B5F'; green='#26A269'; gold='#F5B83D'; pale='#F4F7FC'; gray='#667085'; white='#FFFFFF'

def esc(s): return html.escape(str(s))
def svg_text(x,y,s,size=24,color=ink,weight=400,anchor='start',family='Arial',opacity=1,letter=0):
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="{anchor}" opacity="{opacity}" letter-spacing="{letter}">{esc(s)}</text>'
def multiline(x,y,s,size=24,color=ink,weight=400,width=45,line=1.25,anchor='start'):
    lines=[]
    for p in s.split('\n'):
      lines += textwrap.wrap(p,width=width,break_long_words=False) or ['']
    return ''.join(svg_text(x,y+i*size*line,t,size,color,weight,anchor) for i,t in enumerate(lines))
def rect(x,y,w,h,fill='none',stroke='none',sw=1,rx=0,opacity=1): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"/>'
def circle(x,y,r,fill,opacity=1,stroke='none',sw=1): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{opacity}" stroke="{stroke}" stroke-width="{sw}"/>'
def line(x1,y1,x2,y2,stroke,sw=2,opacity=1,dash=''): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}" stroke-dasharray="{dash}"/>'
def base(): return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="100%" height="100%" fill="{white}"/>'
def save_svg(name,body):
    p=AS/name; p.write_text(base()+body+'</svg>',encoding='utf-8'); return p

def footer(num,source='Аналитика автора на основе семантической карты iFORA; источники — в справке'):
    return line(80,850,1520,850,'#D9E1F2',1)+svg_text(80,878,source,14,gray)+svg_text(1520,878,f'{num:02d}',14,gray,700,'end')

# Slide 1
b=''
b+=rect(0,0,W,H,navy)
b+=f'<defs><radialGradient id="g"><stop offset="0" stop-color="{cyan}" stop-opacity=".95"/><stop offset=".5" stop-color="{blue}" stop-opacity=".5"/><stop offset="1" stop-color="{navy}" stop-opacity="0"/></radialGradient></defs>'
b+=circle(1210,440,350,'url(#g)')
random.seed(12); pts=[]
for i in range(42):
 a=random.random()*math.tau; rr=random.uniform(55,310); x=1210+math.cos(a)*rr; y=435+math.sin(a)*rr*.75; pts.append((x,y))
for i,(x,y) in enumerate(pts):
 for j in range(i):
  x2,y2=pts[j]
  d=((x-x2)**2+(y-y2)**2)**.5
  if d<115: b+=line(x,y,x2,y2,'#76E4F0',1,.28)
for i,(x,y) in enumerate(pts): b+=circle(x,y,random.choice([4,5,7,9]),random.choice([cyan,blue,violet,coral]),.9)
b+=svg_text(85,88,'iFORA × ТРЕНДЫ ИИ',20,cyan,700,letter=2)
b+=multiline(85,205,'Искусственный\nинтеллект — 2026',66,white,700,18,1.08)
b+=multiline(88,390,'От «умных моделей» — к инфраструктуре решений,\nагентам и физическому миру',29,'#C9D5F2',400,50,1.3)
b+=rect(85,590,690,116,'#142650','none',0,18)
b+=svg_text(112,630,'ГЛАВНЫЙ СДВИГ',15,cyan,700,letter=1.5)
b+=multiline(112,670,'Ценность перемещается от качества отдельной модели\nк надежности всей системы: данные → агент → действие.',23,white,600,60,1.25)
b+=svg_text(85,822,'Семантическая карта • кейсы 2026 • стратегия позиционирования iFORA',18,'#8FA3CD')
save_svg('01_title.svg',b)

# Slide 2 map
b=''; b+=svg_text(72,68,'ИИ в 2026: ядро рынка — не модель, а контур принятия решений',35,navy,700)
b+=svg_text(72,105,'Генеративный ИИ соединяет данные, интерфейсы и физические системы; доверие становится условием масштабирования.',20,gray)
clusters=[
 ('ВЫЧИСЛИТЕЛЬНЫЙ\nФУНДАМЕНТ',365,245,126,blue,['облачные платформы','нейроморфные чипы','периферийные вычисления']),
 ('МОДЕЛИ И\nПРЕДСКАЗАНИЕ',665,230,132,violet,['машинное обучение','глубокие сети','прогнозные модели']),
 ('КОМПЬЮТЕРНОЕ\nЗРЕНИЕ',995,250,125,coral,['распознавание объектов','медицинские изображения','3D / дополненная реальность']),
 ('ЧЕЛОВЕК + ИИ',330,535,134,'#2E9E7A',['ИИ-ассистенты','совместная работа','интеллектуальные интерфейсы']),
 ('АВТОНОМНЫЕ\nСИСТЕМЫ',645,560,140,gold,['робототехника','автономный транспорт','удалённый мониторинг']),
 ('ЯЗЫК, РЕЧЬ\nИ МУЛЬТИМОДАЛЬНОСТЬ',985,545,145,cyan,['генеративные модели','перевод и поиск','распознавание речи']),
 ('ДОВЕРЕННЫЙ ИИ',1290,390,116,'#E05178',['безопасность','объяснимость','контроль рисков'])]
# edges
for i,j in [(0,1),(1,2),(0,3),(1,3),(1,4),(1,5),(2,5),(3,4),(3,5),(4,5),(1,6),(2,6),(5,6)]:
 a=clusters[i]; c=clusters[j]; b+=line(a[1],a[2],c[1],c[2],'#C5D0E5',8,.6)
for title,x,y,r,col,tags in clusters:
 b+=circle(x,y,r+16,col,.10); b+=circle(x,y,r,col,.92)
 lines=title.split('\n'); start=y-(len(lines)-1)*15
 for k,t in enumerate(lines): b+=svg_text(x,start+k*30,t,19,white,700,'middle')
 for q,tag in enumerate(tags):
  ang=(-2.4+q*2.4); tx=x+math.cos(ang)*(r+42); ty=y+math.sin(ang)*(r+32)
  b+=circle(tx,ty,7,col); b+=svg_text(tx+(10 if tx>x else -10),ty+5,tag,13,ink,500,'start' if tx>x else 'end')
# insight box
b+=rect(70,720,1110,104,pale,'#DCE5F5',1,16)
b+=svg_text(95,752,'КАК ЧИТАТЬ ЛАНДШАФТ',14,blue,700,letter=1)
b+=multiline(95,785,'Размер узла = значимость темы • расстояние = смысловая близость • цвет = кластер.\nАвторская укрупненная реконструкция исходной карты; названия кластеров переведены на язык управленческих решений.',17,ink,400,115,1.25)
b+=rect(1200,720,320,104,navy,'none',0,16); b+=svg_text(1225,754,'ИНСАЙТ',14,cyan,700,letter=1); b+=multiline(1225,786,'Конкурируют уже не модели,\nа связки «данные–агент–действие».',17,white,600,31,1.2)
b+=footer(2); save_svg('02_semantic_map.svg',b)

# Slide 3 cases
b=''; b+=svg_text(72,68,'Два сигнала 2026: ИИ выходит в физический мир — под контролем',35,navy,700)
b+=svg_text(72,105,'Масштабирование упирается одновременно в вычислительную инфраструктуру и доказуемую надежность.',20,gray)
# left case
for x,col,num,title in [(72,blue,'01','ФИЗИЧЕСКИЙ ИИ'),(820,'#E05178','02','ДОВЕРЕННЫЙ ИИ')]:
 b+=rect(x,150,708,600,white,'#D8E2F2',2,22); b+=rect(x,150,708,12,col,'none',0,6)
 b+=svg_text(x+34,205,num,20,col,700); b+=svg_text(x+90,205,title,17,col,700,letter=1)
if True:
 b+=multiline(106,265,'Роботы и автономные\nсистемы становятся\nновым интерфейсом ИИ',34,navy,700,28,1.15)
 b+=rect(106,415,640,126,pale,'none',0,15); b+=svg_text(130,450,'ПОКАЗАТЕЛЬНЫЙ КЕЙС',14,blue,700,letter=1)
 b+=multiline(130,485,'NVIDIA и General Motors создают AI-модели,\nсимуляции и вычислительные контуры для производства\nи транспорта — от цифрового двойника до автомобиля.',18,ink,500,60,1.25)
 b+=svg_text(106,595,'УПРАВЛЕНЧЕСКИЙ ВЫВОД',14,gray,700,letter=1)
 b+=multiline(106,630,'Инвестиционный фокус: данные реального мира,\nсимуляция, edge-вычисления и безопасность контура.',20,ink,600,55,1.25)
 b+=svg_text(106,714,'Источник: NVIDIA, 18.03.2025 (доступ: 13.08.2026)',13,gray)
 b+=multiline(854,265,'Регулирование становится\nчастью архитектуры\nпродукта — не «комплаенсом»',34,navy,700,29,1.15)
 b+=rect(854,415,640,126,'#FFF4F6','none',0,15); b+=svg_text(878,450,'ПОКАЗАТЕЛЬНЫЙ КЕЙС',14,'#E05178',700,letter=1)
 b+=multiline(878,485,'С 2 августа 2026 г. применяются ключевые правила\nEU AI Act для high-risk систем; поставщикам нужны\nуправление рисками, документация и human oversight.',18,ink,500,61,1.25)
 b+=svg_text(854,595,'УПРАВЛЕНЧЕСКИЙ ВЫВОД',14,gray,700,letter=1)
 b+=multiline(854,630,'Доверие превращается в продуктовую функцию:\ntraceability, оценка качества и контроль человека.',20,ink,600,55,1.25)
 b+=svg_text(854,714,'Источник: European Commission, AI Act (доступ: 13.08.2026)',13,gray)
b+=footer(3); save_svg('03_cases.svg',b)

# Slide 4 positioning
b=''; b+=svg_text(72,68,'iFORA: единый радар решений для государства, бизнеса и науки',35,navy,700)
b+=svg_text(72,105,'Позиционирование: не «поисковик по документам», а доказательная система раннего обнаружения возможностей и рисков.',20,gray)
cols=[(72,blue,'ОРГАНЫ ВЛАСТИ','Боль','Сигналы разрознены;\nрешения запаздывают','Задача','Мониторинг технологий,\nрынков и регуляторных рисков','Ценность','Обоснованные приоритеты\nи измеримый foresight'),(568,violet,'БИЗНЕС','Боль','Сложно отличить тренд\nот информационного шума','Задача','Скаутинг технологий,\nконкурентов и партнеров','Ценность','Быстрее гипотеза →\nпилот → инвестиция'),(1064,'#2E9E7A','НАУКА','Боль','Невидимы смежные фронтиры\nи окна кооперации','Задача','Картирование фронтиров,\nкоманд и патентных ниш','Ценность','Сильнее повестка, заявки\nи междисциплинарные связи')]
for x,col,a,l1,t1,l2,t2,l3,t3 in cols:
 b+=rect(x,160,448,500,white,'#D9E2F2',2,20); b+=rect(x,160,448,82,col,'none',0,20); b+=svg_text(x+28,211,a,21,white,700)
 yy=290
 for lab,txt in [(l1,t1),(l2,t2),(l3,t3)]:
  b+=svg_text(x+30,yy,lab.upper(),13,col,700,letter=1); b+=multiline(x+30,yy+37,txt,20,ink,600,36,1.25); yy+=128
b+=rect(72,700,1440,114,navy,'none',0,18)
b+=svg_text(100,738,'ОБЩЕЕ ОБЕЩАНИЕ',14,cyan,700,letter=1)
b+=multiline(100,778,'iFORA превращает миллионы документов в общую картину — и делает следующий стратегический шаг проверяемым.',25,white,700,100,1.2)
b+=footer(4,'Источник позиционирования: открытые материалы ИСИЭЗ НИУ ВШЭ; синтез автора'); save_svg('04_positioning.svg',b)

# pptx package (SVG full-slide pictures)
def pptx(slides,path):
 ct=['<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">',
 '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="svg" ContentType="image/svg+xml"/>',
 '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>','<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>']
 for i in range(1,len(slides)+1): ct.append(f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>')
 ct.append('</Types>')
 pres='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:sldIdLst>'+''.join(f'<p:sldId id="{255+i}" r:id="rId{i}"/>' for i in range(1,len(slides)+1))+'</p:sldIdLst><p:sldSz cx="12192000" cy="6858000" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>'
 rels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'+''.join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1,len(slides)+1))+'</Relationships>'
 rootrels='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/></Relationships>'
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
  z.writestr('[Content_Types].xml',''.join(ct)); z.writestr('_rels/.rels',rootrels); z.writestr('ppt/presentation.xml',pres); z.writestr('ppt/_rels/presentation.xml.rels',rels)
  for i,s in enumerate(slides,1):
   slide=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr/><p:pic><p:nvPicPr><p:cNvPr id="2" name="Slide {i}"/><p:cNvPicPr/><p:nvPr/></p:nvPicPr><p:blipFill><a:blip r:embed="rId1"/><a:stretch><a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>'''
   sr='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image%d.svg"/></Relationships>'%i
   z.writestr(f'ppt/slides/slide{i}.xml',slide); z.writestr(f'ppt/slides/_rels/slide{i}.xml.rels',sr); z.write(s,f'ppt/media/image{i}.svg')

# minimalist PDF with embedded DejaVu Sans, each SVG represented by executive text blocks (full textual PDF)
def pdf(path):
 font=Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf').read_bytes(); objs=[]
 def add(data): objs.append(data if isinstance(data,bytes) else data.encode()); return len(objs)
 fontid=add(font); desc=add(f'<< /Type /FontDescriptor /FontName /DejaVuSans /Flags 32 /FontBBox [-1021 -463 1793 1232] /ItalicAngle 0 /Ascent 928 /Descent -236 /CapHeight 928 /StemV 80 /FontFile2 {fontid} 0 R >>')
 cid=add(f'<< /Type /Font /Subtype /CIDFontType2 /BaseFont /DejaVuSans /CIDSystemInfo << /Registry (Adobe) /Ordering (Identity) /Supplement 0 >> /FontDescriptor {desc} 0 R /CIDToGIDMap /Identity /DW 600 >>')
 fnt=add(f'<< /Type /Font /Subtype /Type0 /BaseFont /DejaVuSans /Encoding /Identity-H /DescendantFonts [{cid} 0 R] >>')
 pages=[]
 contents=[
 [('ИСКУССТВЕННЫЙ ИНТЕЛЛЕКТ — 2026',38,70,520),('От «умных моделей» — к инфраструктуре решений, агентам и физическому миру',20,70,455),('ГЛАВНЫЙ СДВИГ',15,70,340),('Ценность перемещается от качества отдельной модели к надежности всей системы:',18,70,305),('данные → агент → действие.',24,70,270)],
 [('ИИ в 2026: ядро рынка — не модель, а контур принятия решений',25,55,535),('ВЫЧИСЛИТЕЛЬНЫЙ ФУНДАМЕНТ  •  МОДЕЛИ И ПРЕДСКАЗАНИЕ',18,70,450),('КОМПЬЮТЕРНОЕ ЗРЕНИЕ  •  ЧЕЛОВЕК + ИИ',18,70,400),('АВТОНОМНЫЕ СИСТЕМЫ  •  ЯЗЫК, РЕЧЬ И МУЛЬТИМОДАЛЬНОСТЬ',18,70,350),('ДОВЕРЕННЫЙ ИИ',18,70,300),('Инсайт: конкурируют связки «данные–агент–действие».',20,70,210)],
 [('Два сигнала 2026: ИИ выходит в физический мир — под контролем',25,55,535),('01  ФИЗИЧЕСКИЙ ИИ',19,60,460),('NVIDIA × General Motors: модели, симуляции и вычисления для производства и транспорта.',15,60,420),('Фокус: данные реального мира, симуляция, edge-вычисления, безопасность.',15,60,385),('02  ДОВЕРЕННЫЙ ИИ',19,60,300),('EU AI Act: с 2 августа 2026 г. — ключевые правила для high-risk систем.',15,60,260),('Доверие становится продуктовой функцией: traceability, качество, human oversight.',15,60,225)],
 [('iFORA: единый радар решений для государства, бизнеса и науки',25,55,535),('ОРГАНЫ ВЛАСТИ',19,60,455),('Мониторинг технологий и рисков → обоснованные приоритеты.',15,60,420),('БИЗНЕС',19,60,345),('Скаутинг технологий, конкурентов и партнеров → быстрее к пилоту.',15,60,310),('НАУКА',19,60,235),('Картирование фронтиров и патентных ниш → сильнее повестка и кооперация.',15,60,200)] ]
 for pg in contents:
  commands=['q 1 1 1 rg 0 0 960 540 re f Q','BT /F1 12 Tf 0.045 0.09 0.21 rg']
  for t,sz,x,y in pg:
   hx=t.encode('utf-16-be').hex().upper(); commands+= [f'/F1 {sz} Tf',f'1 0 0 1 {x} {y} Tm <{hx}> Tj']
  commands+=['ET']; stream='\n'.join(commands).encode(); sid=add(b'<< /Length %d >>\nstream\n'%len(stream)+stream+b'\nendstream'); pages.append((sid,None))
 kids=[]
 pagesid=len(objs)+len(pages)+1
 for sid,_ in pages:
  pid=add(f'<< /Type /Page /Parent {pagesid} 0 R /MediaBox [0 0 960 540] /Resources << /Font << /F1 {fnt} 0 R >> >> /Contents {sid} 0 R >>'); kids.append(pid)
 actualpages=add(f'<< /Type /Pages /Kids [{" ".join(str(x)+" 0 R" for x in kids)}] /Count {len(kids)} >>')
 # Parent refs calculated correctly because contents existed first and pagesid points first after adding page objs? Fix page parent refs via replacement.
 for pid in kids: objs[pid-1]=objs[pid-1].replace(f'/Parent {pagesid} 0 R'.encode(),f'/Parent {actualpages} 0 R'.encode())
 catalog=add(f'<< /Type /Catalog /Pages {actualpages} 0 R >>')
 out=bytearray(b'%PDF-1.7\n%\xe2\xe3\xcf\xd3\n'); offs=[0]
 for i,o in enumerate(objs,1): offs.append(len(out)); out+=f'{i} 0 obj\n'.encode()+o+b'\nendobj\n'
 xref=len(out); out+=f'xref\n0 {len(objs)+1}\n0000000000 65535 f \n'.encode()
 for q in offs[1:]: out+=f'{q:010d} 00000 n \n'.encode()
 out+=f'trailer << /Size {len(objs)+1} /Root {catalog} 0 R >>\nstartxref\n{xref}\n%%EOF'.encode(); path.write_bytes(out)

# docx
def docx(path):
 paras=[]
 def p(text='',style=None,bold=False):
  pr=f'<w:pPr><w:pStyle w:val="{style}"/></w:pPr>' if style else ''
  rpr='<w:rPr><w:b/></w:rPr>' if bold else ''
  paras.append(f'<w:p>{pr}<w:r>{rpr}<w:t xml:space="preserve">{html.escape(text)}</w:t></w:r></w:p>')
 p('АНАЛИТИЧЕСКАЯ СПРАВКА','Title'); p('Тренды искусственного интеллекта в мире: интерпретация семантической карты iFORA, 2020–2026 гг.','Subtitle'); p('Подготовлено для топ-менеджмента • 13 августа 2026 г.')
 p('Резюме для принятия решений','Heading1');
 for s in ['1. Центр тяжести ИИ смещается от соревнования отдельных моделей к архитектуре решений: вычисления, данные, агентный слой, интерфейс и контроль действия.','2. На карте генеративные модели занимают связующее положение между языком, поиском, изображениями и ассистентами. Их роль — универсальный интерфейс к корпоративному знанию и рабочим процессам.','3. Следующая волна коммерциализации — физический ИИ: автономный транспорт, робототехника, компьютерное зрение, edge-вычисления и цифровые двойники образуют единый контур.','4. Доверие становится ограничивающим ресурсом. Без управления рисками, качества данных, прослеживаемости и human oversight масштабирование в чувствительных сферах невозможно.','5. Для iFORA окно позиционирования — «радар доказательных решений»: система не только обнаруживает слабые сигналы, но и связывает их с субъектами, рынками, технологиями и сценариями действия.']: p(s)
 p('1. Методика и ограничения интерпретации','Heading1'); p('Исходная семантическая карта автоматически сформирована системой iFORA по результатам обработки миллионов англоязычных документов — научных публикаций, патентов и материалов отраслевой рыночной аналитики за 2020–2026 гг. Круговой значок отражает отдельную тематику; его размер и размер подписи пропорциональны значимости темы; расстояние показывает смысловую близость; цвет объединяет близкие темы в кластер.')
 p('Для управленческого слайда выполнена экспертная агрегация: автоматические англоязычные метки сведены в семь емких русскоязычных кластеров. Это не повторное моделирование исходного корпуса и не рейтинг рынков. Карта показывает структуру дискурса и взаимосвязи, но сама по себе не доказывает темпы роста, причинность или инвестиционную привлекательность. Кейсы используются как внешняя проверка актуальности выводов.')
 p('2. Семь контуров технологического ландшафта','Heading1')
 sections=[('Вычислительный фундамент','Облачные платформы, нейроморфные и специализированные чипы, периферийные вычисления. Значимость этого контура объясняется ростом требований к обучению и инференсу, а также переносом части вычислений ближе к устройству.'),('Модели и предсказание','Машинное обучение, глубокие нейронные сети, прогнозное и статистическое моделирование. Это методическое ядро карты, связанное практически со всеми прикладными направлениями.'),('Язык, речь и мультимодальность','Генеративные модели, перевод, поиск и извлечение информации, распознавание и синтез речи. Контур становится универсальным интерфейсом для работы с неструктурированными данными.'),('Компьютерное зрение','Распознавание объектов и лиц, медицинские изображения, обнаружение аномалий, 3D и дополненная реальность. Близость к автономным системам указывает на переход от анализа изображения к действию.'),('Человек + ИИ','Ассистенты, совместная работа, интеллектуальные интерфейсы и human–AI interaction. Ценность возникает не из полной замены человека, а из перераспределения задач и повышения качества решений.'),('Автономные системы','Робототехника, автономный транспорт, удаленный мониторинг и управление. Этот кластер интегрирует модели, сенсоры, зрение, вычисления на устройстве и контуры безопасности.'),('Доверенный ИИ','Безопасность, объяснимость, устойчивость, управление рисками и человеческий контроль. На управленческом уровне это горизонтальный слой, пересекающий все кластеры.')]
 for h,t in sections: p(h,'Heading2'); p(t)
 p('3. Два показательных кейса','Heading1'); p('Кейс 1. NVIDIA и General Motors: физический ИИ','Heading2'); p('18 марта 2025 г. NVIDIA и General Motors объявили о сотрудничестве в области AI-моделей, симуляционных инструментов и ускоренных вычислительных систем для производства и транспорта. Кейс показателен не отдельной моделью, а полной технологической связкой: цифровые двойники производственных линий, обучение роботизированных систем, моделирование автономного транспорта и вычисления на борту. В 2026 г. это подтверждает актуальность плотной зоны карты между компьютерным зрением, автономными системами и вычислительным фундаментом. Управленческий вывод: капиталоемкость и требования к данным реального мира создают барьер для «легкого» входа; приоритетны партнерства и платформенные компетенции.')
 p('Кейс 2. EU AI Act: доверие как часть продукта','Heading2'); p('Европейская комиссия указывает, что основная масса положений AI Act применяется с 2 августа 2026 г., при поэтапном графике отдельных обязательств. Для высокорисковых систем регулирование закрепляет риск-ориентированную логику, требования к данным, документации, прозрачности, человеческому контролю, точности и кибербезопасности. Следовательно, «доверенный ИИ» нельзя выносить в финальный юридический чек-лист: он должен проектироваться одновременно с моделью и бизнес-процессом. Для поставщиков это повышает ценность traceability, оценки качества и мониторинга после внедрения.')
 p('4. Управленческие выводы и действия','Heading1');
 for s in ['Портфель. Оценивать инициативы по полноте контура «данные — модель — интеграция — действие — контроль», а не по эффектности демонстрации.','Инфраструктура. Разделять стратегические инвестиции в вычисления и данные от быстро заменяемого модельного слоя; заранее оценивать зависимость от поставщика.','Продукт. Выбирать процессы с измеримым качеством решения, приемлемой стоимостью ошибки и возможностью человеческой эскалации.','Риск. Ввести единый реестр AI-систем, классификацию риска, владельца модели, журналирование и регулярную проверку качества.','Мониторинг. Обновлять карту ежеквартально и накладывать на нее патентную динамику, научные фронтиры, инвестиции и регуляторные события.']: p(s)
 p('5. Позиционирование iFORA','Heading1'); p('Органам власти iFORA помогает переводить разрозненные сигналы в доказательные приоритеты научно-технологической политики. Бизнесу — отличать устойчивые технологические сдвиги от шума, находить партнеров и сокращать путь от гипотезы к пилоту. Научным организациям — видеть смежные фронтиры, перспективные команды и патентные ниши. Общее обещание бренда: «iFORA превращает миллионы документов в общую картину и делает следующий стратегический шаг проверяемым».')
 p('Источники','Heading1')
 refs=['1. ИСИЭЗ НИУ ВШЭ. iFORA — система интеллектуального анализа больших данных [Электронный ресурс]. URL: https://issek.hse.ru/fora/ (дата обращения: 13.08.2026).','2. European Commission. AI Act [Electronic resource]. URL: https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai (accessed: 13.08.2026).','3. NVIDIA. NVIDIA and General Motors Collaborate on AI for Next-Generation Vehicle Experience and Manufacturing [Electronic resource]. 18 March 2025. URL: https://nvidianews.nvidia.com/news/gm-collaboration (accessed: 13.08.2026).','4. Stanford Institute for Human-Centered AI. AI Index Report 2025 [Electronic resource]. URL: https://hai.stanford.edu/ai-index/2025-ai-index-report (accessed: 13.08.2026).','5. OECD. OECD AI Principles [Electronic resource]. URL: https://oecd.ai/en/ai-principles (accessed: 13.08.2026).','6. NIST. Artificial Intelligence Risk Management Framework (AI RMF 1.0). Gaithersburg, MD: National Institute of Standards and Technology, 2023. DOI: 10.6028/NIST.AI.100-1.']
 for s in refs:p(s)
 p('Примечание об источниках','Heading2'); p('Ссылки оформлены в приближенном к ГОСТ Р 7.0.100–2018 виде для электронных ресурсов. Фактические формулировки по кейсам следует сверять по указанным первичным источникам перед публичным распространением. Аналитические выводы и русскоязычные названия кластеров являются авторской интерпретацией исходной карты iFORA.')
 body=''.join(paras)
 doc=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{body}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr></w:body></w:document>'''
 styles='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial"/><w:sz w:val="22"/></w:rPr><w:pPr><w:spacing w:after="120" w:line="300" w:lineRule="auto"/><w:jc w:val="both"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:color w:val="0B1736"/><w:sz w:val="44"/></w:rPr><w:pPr><w:spacing w:after="180"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:color w:val="3366FF"/><w:sz w:val="28"/></w:rPr></w:style><w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:rPr><w:b/><w:color w:val="0B1736"/><w:sz w:val="30"/></w:rPr><w:pPr><w:spacing w:before="260" w:after="120"/></w:pPr></w:style><w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:rPr><w:b/><w:color w:val="3366FF"/><w:sz w:val="24"/></w:rPr><w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr></w:style></w:styles>'''
 ct='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>'
 rel='<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:z.writestr('[Content_Types].xml',ct);z.writestr('_rels/.rels',rel);z.writestr('word/document.xml',doc);z.writestr('word/styles.xml',styles)

slides=[AS/f'{i:02d}_{n}.svg' for i,n in [(1,'title'),(2,'semantic_map'),(3,'cases'),(4,'positioning')]]
outputs=[OUT/'IFORA_AI_Trends_2026.pptx',OUT/'IFORA_AI_Trends_2026.pdf',OUT/'IFORA_AI_Trends_2026_analytical_note.docx']
pptx(slides,outputs[0]); pdf(outputs[1]); docx(outputs[2])
archive=OUT/'deliverables_bundle.tar.gz'
with tarfile.open(archive,'w:gz') as bundle:
 for output in outputs: bundle.add(output,arcname=output.name)
encoded=base64.encodebytes(archive.read_bytes())
(OUT/'deliverables_bundle.tar.gz.b64').write_bytes(encoded)
archive.unlink()
for output in outputs: output.unlink()
print('Generated:',OUT/'deliverables_bundle.tar.gz.b64')
