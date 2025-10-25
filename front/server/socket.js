import { Server } from "socket.io";
import fs from "fs";
import path from "path";

const dataDir = path.join(process.cwd(), "server/data");
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

export function initSocket(httpServer) {
  const io = new Server(httpServer);
  const rooms = {}; // { roomId: { password, users: [], messages: [] } }

  io.on("connection", (socket) => {
    let currentRoom = null;

    socket.on("join-room", ({ roomId, userName, password, avatar }) => {
      currentRoom = roomId;

      if (rooms[roomId] && rooms[roomId].password !== password) {
        socket.emit("password-error", "Неверный пароль для этой комнаты");
        return;
      }

      if (!rooms[roomId]) rooms[roomId] = { users: [], messages: [], password };
      rooms[roomId].users.push({ id: socket.id, name: userName, avatar, muted: false, video: true });

      const filePath = path.join(dataDir, `${roomId}.json`);
      if (fs.existsSync(filePath)) {
        rooms[roomId].messages = JSON.parse(fs.readFileSync(filePath));
      }

      socket.emit("chat-history", rooms[roomId].messages);
      io.to(currentRoom).emit("users-update", rooms[roomId].users);
      socket.to(currentRoom).emit("user-joined", { id: socket.id, name: userName, avatar });
    });

    // WebRTC сигналы
    socket.on("webrtc-offer", (data) => socket.to(data.target).emit("webrtc-offer", { sdp: data.sdp, from: socket.id }));
    socket.on("webrtc-answer", (data) => socket.to(data.target).emit("webrtc-answer", { sdp: data.sdp, from: socket.id }));
    socket.on("ice-candidate", (data) => socket.to(data.target).emit("ice-candidate", { candidate: data.candidate, from: socket.id }));

    // Чат
    socket.on("send-message", (msg) => {
      if (!currentRoom) return;
      const message = { id: Date.now(), text: msg.text, user: msg.user, time: new Date().toLocaleTimeString() };
      rooms[currentRoom].messages.push(message);
      fs.writeFileSync(path.join(dataDir, `${currentRoom}.json`), JSON.stringify(rooms[currentRoom].messages, null, 2));
      io.to(currentRoom).emit("new-message", message);
    });

    // Обновление статусов (выключение/включение микрофона или видео)
    socket.on("update-status", (data) => {
      if(!currentRoom) return;
      const user = rooms[currentRoom].users.find(u => u.id === socket.id);
      if(user){
        if(data.hasOwnProperty('muted')) user.muted = data.muted;
        if(data.hasOwnProperty('video')) user.video = data.video;
      }
      io.to(currentRoom).emit("users-update", rooms[currentRoom].users);
    });

    socket.on("disconnect", () => {
      if (!currentRoom) return;
      rooms[currentRoom].users = rooms[currentRoom].users.filter(u => u.id !== socket.id);
      io.to(currentRoom).emit("users-update", rooms[currentRoom].users);
      io.to(currentRoom).emit("user-left", { id: socket.id });
    });
  });
}
