import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import http from "http";
import { initSocket } from "./server/socket.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const server = http.createServer(app);

app.use(express.static(path.join(__dirname, "client")));

initSocket(server);

const PORT = process.env.PORT || 3000;
server.listen(PORT, () => console.log(`Server started on port ${PORT}`));
