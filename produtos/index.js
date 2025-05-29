const express = require('express');
const app = express();
const port = 3000;

app.get('/products', (req, res) => {
  res.json({
    produtos: [
      { id: 1, name: 'Notebook', price: 3000 },
      { id: 2, name: 'Mouse', price: 100 }
    ]
  });
});

app.listen(port, () => {
  console.log(`API de Produtos rodando em http://localhost:${port}`);
});
