// Canonical iztro (npm) Zi Wei Dou Shu chart. Usage: node ziwei.js YYYY-M-D timeIndex gender lang [horoscopeDate...]
const { astro } = require("iztro");
const [date, ti, gender, lang, ...hdates] = process.argv.slice(2);
const a = astro.bySolar(date, Number(ti), gender, true, lang);
const out = {
  iztro_version: require("iztro/package.json").version,
  solarDate: a.solarDate, lunarDate: a.lunarDate, chineseDate: a.chineseDate, time: a.time, timeRange: a.timeRange,
  sign: a.sign, zodiac: a.zodiac, soul: a.soul, body: a.body, fiveElementsClass: a.fiveElementsClass,
  earthlyBranchOfSoulPalace: a.earthlyBranchOfSoulPalace, earthlyBranchOfBodyPalace: a.earthlyBranchOfBodyPalace,
  palaces: a.palaces.map(p => ({
    index: p.index, name: p.name, isBodyPalace: p.isBodyPalace, isOriginalPalace: p.isOriginalPalace,
    heavenlyStem: p.heavenlyStem, earthlyBranch: p.earthlyBranch,
    majorStars: p.majorStars.map(s => ({ name: s.name, type: s.type, brightness: s.brightness, mutagen: s.mutagen })),
    minorStars: p.minorStars.map(s => ({ name: s.name, type: s.type, brightness: s.brightness, mutagen: s.mutagen })),
    decadal: p.decadal, ages: p.ages,
  })),
  horoscopes: hdates.map(d => {
    const h = a.horoscope(d);
    const pick = x => ({ index: x.index, name: x.name, heavenlyStem: x.heavenlyStem, earthlyBranch: x.earthlyBranch, mutagen: x.mutagen, palaceNames: x.palaceNames });
    return { date: d, nominalAge: h.age && h.age.nominalAge, decadal: pick(h.decadal), yearly: pick(h.yearly) };
  }),
};
console.log(JSON.stringify(out));
