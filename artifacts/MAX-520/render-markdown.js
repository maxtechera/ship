const fs = require('fs');
const { marked } = require('marked');
const md = fs.readFileSync('artifacts/MAX-520/HANDOFF.md', 'utf8');
const body = marked.parse(md);
const html = `<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>MAX-520 handoff render</title>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.8.1/github-markdown-light.min.css">
  <style>
    body { box-sizing: border-box; min-width: 200px; max-width: 980px; margin: 0 auto; padding: 32px; }
  </style>
</head>
<body>
  <article class="markdown-body">
${body}
  </article>
</body>
</html>
`;
fs.writeFileSync('artifacts/MAX-520/rendered-github-markdown.html', html);
