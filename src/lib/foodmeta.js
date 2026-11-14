// Einordnung von Lebensmitteln für Listen: Einkaufskategorie und Hauptnährstoff.
// Bewusst ohne Import der Lebensmitteldatenbank, damit der Planer sie nicht mitladen muss.
import { icon } from './icons.js';

/** Einkaufskategorien in Anzeigereihenfolge: [Schlüssel, Überschrift, Icon, Gruppen aus tools/foods_src.py]. */
export const CATS = [
  ['gemuese', 'Gemüse, Salat und Pilze', 'leaf', ['gemuese', 'blatt', 'pilze', 'knolle']],
  ['saettig', 'Hülsenfrüchte, Getreide, Soja und Suppen', 'pot', ['huelsen', 'getreide', 'soja', 'knusper', 'suppe']],
  ['nuss', 'Nüsse, Saaten und Oliven', 'nut', ['nuss', 'fettfrucht']],
  ['oel', 'Öle', 'oil', ['fett']],
  ['pflanz', 'Pflanzliche Joghurts und Cremes', 'cup', ['pflanz']],
  ['obst', 'Obst', 'apple', ['obst']],
  ['wuerze', 'Kräuter und Würzen', 'herb', ['kraeuter', 'wuerze']],
  ['trinken', 'Getränke', 'cup', ['getraenk']],
  ['tauschen', 'Passt nicht ins Scheinfasten', 'ban', ['tier', 'milch', 'suess', 'weissmehl', 'drink', 'eiweiss', 'fertig']],
];
const CAT_OF_GROUP = Object.fromEntries(CATS.flatMap(([k, , , gs]) => gs.map((g) => [g, k])));

/** Kategorie-Schlüssel eines Lebensmittels (Objekt mit group). */
export const catOf = (f) => CAT_OF_GROUP[f?.group] || 'gemuese';

/** Sortiert eine Liste in Kategorien. get(item) liefert das Lebensmittel-Objekt. Leere Kategorien fallen weg. */
export function groupByCat(items, get) {
  const out = CATS.map(([key, label, icon]) => ({ key, label, icon, items: [] }));
  const idx = Object.fromEntries(out.map((c, i) => [c.key, i]));
  for (const it of items) out[idx[catOf(get(it))]].items.push(it);
  return out.filter((c) => c.items.length);
}

export const MACROS = { carbs: 'Kohlenhydrate', protein: 'Eiweiß', fat: 'Fett' };

/**
 * Hauptnährstoff eines Lebensmittels: der Makronährstoff mit dem größten Anteil an den Kalorien.
 * n = [kcal, Eiweiß, Fett, Kohlenhydrate, ...] je 100 g. Kräuter, Würzen und fast kalorienfreie
 * Lebensmittel bekommen kein Symbol, weil sie in üblichen Mengen kaum etwas beitragen.
 * Rückgabe: { key, share } oder null.
 */
export function macroOf(f) {
  if (!f?.n || ['kraeuter', 'wuerze'].includes(f.group)) return null;
  const [, p, fa, c] = f.n;
  const e = { carbs: c * 4, protein: p * 4, fat: fa * 9 };
  const t = e.carbs + e.protein + e.fat;
  if (t < 10) return null;
  const [key, v] = Object.entries(e).sort((a, b) => b[1] - a[1])[0];
  return { key, share: Math.round((v / t) * 100) };
}

// Symbol je Lebensmittel: Regeln nach Name (erste passende gewinnt), sonst nach Gruppe.
const RULES = [
  // Vorrangige Einzelfälle, damit Namensbestandteile nicht falsch greifen
  [/Käsekuchen|Apfelstrudel/, 'cake'],
  [/Glühwein/, 'wine'],
  [/Getreidekaffee/, 'cup'],
  [/Kaffeesahne|Reis-Kokos-Drink/, 'carton'],
  [/Kartoffelpüree|Kartoffelsalat/, 'potato'],
  [/Haferbrei/, 'bowl'],
  [/Räucherlachs/, 'fish'],
  [/Röstzwiebeln/, 'onion'],
  [/Erdnussflips/, 'chips'],
  [/Cornflakes/, 'carbs'],
  [/Vollkornreis|Wildreis/, 'bowl'],
  [/Vollkornbrötchen/, 'bread'],
  [/Agavendicksaft/, 'bottle'],
  [/Kakaogetränk/, 'chocolate'],
  [/Schattenmorellen/, 'berries'],
  [/Kandierter Ingwer/, 'candy'],
  [/[Ss]prossen/, 'sprout'],
  [/[Mm]elone/, 'melon'],
  [/Weintraube/, 'berries'],
  [/Zuckerschote/, 'pod'],
  [/Leberkäse/, 'meat'],
  [/Buttermilch/, 'carton'],
  [/Weinessig/, 'bottle'],
  [/[Ss]chokolade/, 'chocolate'],
  [/Studentenfutter|Gebrannte Mandeln/, 'nut'],
  [/Datteln|Getrocknete (Aprikosen|Feigen|Mango)|Apfelringe/, 'apple'],
  [/[Zz]wiebel/, 'onion'],
  [/[Ss]ellerie/, 'carrot'],
  [/[Kk]äse|Camembert|Gorgonzola|Halloumi|Ricotta|Mozzarella|Feta|Parmesan|Emmentaler|Edamer|Cheddar|Tilsiter|Brie|Obazda|Mascarpone|Raclette/, 'cheese'],
  [/^Butter$|Kräuterbutter|Butterschmalz|Halbfettbutter/, 'butter'],
  [/Dickmilch|Sahnequark|Saure Sahne|Schmand/, 'yogurt'],
  [/suppe|Eintopf|Chili sin|Chili con|Gulasch|Minestrone|Ratatouille|Gazpacho|Brühe|brühe/, 'soup'],
  [/Kaffee|Espresso|Cappuccino/, 'cup'],
  [/tee$|Tee$|Mate/, 'tea'],
  [/Kokosmilch|Kokosnuss|Kokosraspeln|Kokoschips|Kokosmus|Kokosmehl|Kokoswasser/, 'coconut'],
  [/drink|Milch|milch$|Kefir|Buttermilch|Ayran|Sahne|Kaffeesahne/, 'carton'],
  [/joghurt|Joghurt|quark|Quark|Skyr|Pudding|Schlagcreme|Kochcreme|kochcreme|Dickmilch|Schmand|Saure Sahne|Crème|Frischkäse|Milchreis|Rote Grütze/, 'yogurt'],
  [/Käse|Camembert|Gorgonzola|Halloumi|Ricotta|Mozzarella|Feta|Parmesan|Emmentaler|Edamer|Cheddar|Tilsiter|Brie|Obazda|Mascarpone|Raclette/, 'cheese'],
  [/Saft|saft|Wasser|wasser|Cola|Limonade|Schorle|Eistee|Tonic|Smoothie|Kombucha|shake|Kakaogetränk|Malzbier/, 'water'],
  [/Bier|Wein|Sekt|Spirituosen|Radler/, 'wine'],
  [/sauce|Sauce|Sojasauce|Essig|essig|Balsamico|Sriracha|Worcester|Dressing|Salatcreme|Sirup|sirup|dicksaft|Bratensoße/, 'bottle'],
  [/mus$|Tahin|Streichcreme|Erdnussbutter|aufstrich|Hummus|Pastete|Guacamole|Ajvar|Senf|Marmelade|Nougat|Pesto|Chutney|Wasabi|Meerrettich|Tomatenmark|Misopaste|Currypaste|Mayonnaise|Remoulade|Ketchup|Honig|Glas\)|Mixed Pickles|Puszta|Kimchi|Sambal/, 'jar'],
  [/pulver|Kurkuma|Kreuzkümmel|Zimt|Pfeffer$|Salz$|Muskat|Oregano|Hefeflocken|Chiliflocken|Gelatine/, 'shaker'],
  [/Oliven|Kapern/, 'olive'],
  [/Avocado/, 'avocado'],
  [/Leinsamen|Chiasamen|Sesam|Hanfsamen|Mohn|Kürbiskerne|Sonnenblumenkerne|Pinienkerne/, 'seeds'],
  [/ürbis/, 'pumpkin'],
  [/Maiswaffel|Reiswaffel|Waffel/, 'ricecake'],
  [/Knäckebrot|Cracker|Zwieback|Salzstangen/, 'cracker'],
  [/Chips|chips|Flips|Sticks|Pommes|Erdnüsse im Teigmantel/, 'chips'],
  [/omate/, 'tomato'],
  [/Paprika|Peperoni/, 'pepper'],
  [/Chili|Sambal/, 'chili'],
  [/Brokkoli|Romanesco|Blumenkohl/, 'broccoli'],
  [/kohl|Kohl|Pak Choi|Wirsing|Sauerkraut/, 'cabbage'],
  [/Zwiebel|Knoblauch|Schalotte|Lauch/, 'onion'],
  [/Karotte|Möhre|Pastinake|Petersilienwurzel|Rote Bete|Rübe|Steckrübe|Sellerie|Rettich|Radieschen|Schwarzwurzel|Topinambur|Ingwer|Suppengemüse/, 'carrot'],
  [/Kartoffel|Süßkartoffel|Maniok|Rösti|Kroketten|Gnocchi|Klöße|Maronen/, 'potato'],
  [/Mais|Polenta|Popcorn/, 'corn'],
  [/Zucchini|Gurke|Cornichon|gurken/, 'cucumber'],
  [/Aubergine/, 'eggplant'],
  [/Pilz|pilz|Champignon|Shiitake|Pfifferling/, 'mushroom'],
  [/Bohne|bohne|Erbse|erbse|Linse|Edamame|Falafel|Lupine|Baked Beans|Allerlei/, 'pod'],
  [/Tofu|Tempeh|Seitan|Soja|Veggie-|Vegane Würstchen|Veganes Schnitzel|Proteinpulver/, 'tofu'],
  [/mehl|Stärke|flocken|Flocken|Müsli|müsli|kleie|Weizenkeime|gepufft/, 'carbs'],
  [/Reis|Quinoa|Hirse|Bulgur|Couscous|Buchweizen|Amaranth|Grünkern|Dinkel|Graupen|Haferbrei|Risotto|Paella|Sushi|nudeln|Nudeln|Ravioli/, 'bowl'],
  [/brot|Brot|Brötchen|Baguette|Croissant|Brezel|Wraps|Pumpernickel|Blätterteig/, 'bread'],
  [/Pizza/, 'pizza'],
  [/Beere|beere|Kirsche|kirsche|Schattenmorellen|Cranberr|Physalis|Litschi|Mirabelle|Pflaume|Weintraube|Rosinen/, 'berries'],
  [/Banane|banane/, 'banana'],
  [/Orange|Mandarine|Clementine|Grapefruit|Pomelo|Zitrone|Limette/, 'citrus'],
  [/Melone/, 'melon'],
  [/Salat|salat|Spinat|Rucola|Mangold|Chicorée|Radicchio|Kresse|Löwenzahn|Portulak|Nori/, 'leaf'],
  [/sprossen|Sprossen|Spargel|Bambus/, 'sprout'],
  [/Schokolade|Schokoriegel|Pralinen|Schokokuss|Kakaopulver/, 'chocolate'],
  [/Kuchen|kuchen|Strudel|Donut|Kekse|Brownies|Müsliriegel|Fruchtschnitte/, 'cake'],
  [/eis$|Speiseeis|Sorbet/, 'icecream'],
  [/Zucker|zucker|Süßstoff|Xylit|Bonbon|Gummibärchen|Marzipan|Kandierter/, 'candy'],
  [/Lachs|Thunfisch|Garnelen|Fisch|Hering|Makrele|Sardinen|Kabeljau|Muscheln|Tintenfisch|Surimi/, 'fish'],
  [/^Eier$|Eiklar/, 'egg'],
  [/Hähnchen|Rind|Schwein|Salami|Schinken|Burger|Döner|Wurst|wurst|Speck|Frikadelle|Lamm|Ente|Pute|Kasseler|Leberkäse|Würstchen|Bolognese|Schmalz|Hühner|Fleisch|Aufschnitt/, 'meat'],
];
const GROUP_ICON = {
  gemuese: 'leaf', blatt: 'leaf', kraeuter: 'herb', pilze: 'mushroom', knolle: 'potato', huelsen: 'pod', getreide: 'carbs', soja: 'tofu',
  nuss: 'nut', fettfrucht: 'olive', fett: 'oil', obst: 'apple', getraenk: 'water', wuerze: 'jar', knusper: 'ricecake', suppe: 'soup',
  pflanz: 'yogurt', suess: 'candy', weissmehl: 'bread', tier: 'meat', milch: 'carton', drink: 'water', eiweiss: 'tofu', fertig: 'soup',
};
/** Symbolname eines Lebensmittels (immer gesetzt). */
export function foodIcon(name, f) {
  const g = f?.group;
  if (g === 'fett') return /Margarine|Butter|Pflanzencreme|Kokosfett|Halbfett|Schmalz/.test(name) ? 'butter' : 'oil';
  if (g === 'kraeuter') return 'herb';
  if (g === 'nuss' && !/mus$|Tahin|Streichcreme|Erdnussbutter|Leinsamen|Chiasamen|Sesam|Hanfsamen|Mohn|kerne|Käse/.test(name)) return 'nut';
  for (const [re, ic] of RULES) if (re.test(name)) return ic;
  return GROUP_ICON[g] || 'leaf';
}

/**
 * Rundes Symbol vor einem Lebensmittel: Bild = Lebensmittelart, Farbe = Hauptnährstoff
 * (Kohlenhydrate, Eiweiß, Fett; grau bei Kräutern, Würzen und fast Kalorienfreiem).
 */
export function foodBadge(name, f) {
  const m = macroOf(f);
  const lbl = m ? MACROS[m.key] : '';
  const title = m ? `${name}: liefert vor allem ${lbl} (${m.share} % der Kalorien)` : `${name}: kaum Kalorien`;
  return `<span class="mac ${m ? m.key : 'zero'}" title="${title.replace(/"/g, '&quot;')}">${icon(foodIcon(name, f))}${m ? `<span class="sr-only">${lbl}:</span>` : ''}</span>`;
}
