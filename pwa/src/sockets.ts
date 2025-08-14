/**
 * Socket.IO client stub. We’ll subscribe to `hit_detected` in M3.
 */
import { io } from "socket.io-client";

const SOCKET_URL = import.meta.env.VITE_API_BASE?.replace('http', 'ws') || 'ws://localhost:5001';
export const socket = io(SOCKET_URL, { transports: ["websocket"] });
