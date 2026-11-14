import assert from 'node:assert/strict';

function contrast(a, b) {
  const luminance = rgb => rgb.map(v => v / 255).map(v => v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)
    .reduce((sum, v, i) => sum + v * [0.2126, 0.7152, 0.0722][i], 0);
  const [low, high] = [luminance(a), luminance(b)].sort((x, y) => x - y);
  return (high + 0.05) / (low + 0.05);
}

export async function checkThemeColors(page, scheme) {
  const { placeholder, background } = await page.locator('#search-input').evaluate(input => {
    const rgb = color => color.match(/[\d.]+/g).slice(0, 3).map(Number);
    let parent = input;
    while (getComputedStyle(parent).backgroundColor === 'rgba(0, 0, 0, 0)') parent = parent.parentElement;
    return { placeholder: rgb(getComputedStyle(input, '::placeholder').color), background: rgb(getComputedStyle(parent).backgroundColor) };
  });
  assert(contrast(placeholder, background) >= 4.5, `${scheme} search placeholder has insufficient contrast`);

  const line = scheme === 'dark' ? [166, 161, 173] : [92, 89, 98];
  const surface = scheme === 'dark' ? [48, 45, 54] : [245, 246, 250];
  const text = scheme === 'dark' ? [230, 225, 232] : [39, 38, 43];
  assert(contrast(line, background) >= 3 && contrast(line, surface) >= 3, `${scheme} diagram boundaries have insufficient contrast`);
  assert(contrast(text, surface) >= 4.5, `${scheme} diagram labels have insufficient contrast`);
  // Inspect the embedded image's rendered pixels, including manual theme overrides.
  const image = page.locator('figure.mermaid img').first();
  const pixels = await image.screenshot({ animations: 'disabled' });
  const matches = await page.evaluate(async ({ png, colors }) => {
    const image = new Image();
    image.src = `data:image/png;base64,${png}`;
    await image.decode();
    const canvas = document.createElement('canvas');
    canvas.width = image.width; canvas.height = image.height;
    const context = canvas.getContext('2d');
    context.drawImage(image, 0, 0);
    const data = context.getImageData(0, 0, canvas.width, canvas.height).data;
    return colors.map((color, index) => {
      let count = 0;
      for (let i = 0; i < data.length; i += 4) {
        if (!color.every((value, channel) => value === data[i + channel])) continue;
        // A solid legacy fill has adjacent pixels; isolated antialiasing colors do not.
        if (index === 2 && ![4, canvas.width * 4, canvas.width * 4 + 4]
          .every(offset => color.every((value, channel) => value === data[i + offset + channel]))) continue;
        count++;
      }
      return count;
    });
  }, { png: pixels.toString('base64'), colors: [line, surface, [238, 238, 238]] });
  assert(matches[2] === 0, `${scheme} diagram retained a light-only node background`);
  assert(matches.slice(0, 2).every(count => count > 0), `${scheme} diagram did not render its theme's lines and surfaces`);
}
