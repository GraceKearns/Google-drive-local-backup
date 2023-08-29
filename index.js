var express = require('express');
var app = express();
const PORT = 3002
      
  // serve your css as static 
  app.get("/api", (req, res) => {
    res.json({ message: "Hello from server!" });
  });
  
  app.listen(PORT, () => {
    console.log(`Server listening on ${PORT}`);
  });
