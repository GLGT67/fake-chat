// Svelte 5 Reactive State Store for Fake Chat Messenger

export const DEFAULT_AVATARS = [
  "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces"
];

export const THEMES = {
  classic: {
    id: "classic",
    name: "Classic Blue",
    gradient: "from-[#0084FF] to-[#0099FF]",
    primary: "#0084FF",
    bgRight: "bg-[#0084FF]",
    textRight: "text-white"
  },
  ocean: {
    id: "ocean",
    name: "Ocean Purple",
    gradient: "from-[#7F00FF] via-[#0072FF] to-[#00C6FF]",
    primary: "#7F00FF",
    bgRight: "bg-gradient-to-br from-[#7F00FF] to-[#0072FF]",
    textRight: "text-white"
  },
  berry: {
    id: "berry",
    name: "Berry Pink",
    gradient: "from-[#FF2A6D] via-[#9B00E8] to-[#05D9E8]",
    primary: "#FF2A6D",
    bgRight: "bg-gradient-to-r from-[#FF2A6D] to-[#9B00E8]",
    textRight: "text-white"
  },
  sunset: {
    id: "sunset",
    name: "Sunset Peach",
    gradient: "from-[#FA709A] to-[#FEE140]",
    primary: "#FA709A",
    bgRight: "bg-gradient-to-r from-[#FA709A] to-[#FEE140]",
    textRight: "text-white"
  },
  mint: {
    id: "mint",
    name: "Neon Mint",
    gradient: "from-[#00F260] to-[#0575E6]",
    primary: "#00F260",
    bgRight: "bg-gradient-to-r from-[#00F260] to-[#0575E6]",
    textRight: "text-white"
  }
};

export const chatState = $state({
  // Profile settings
  partnerName: "Hoàng Thảo My",
  partnerAvatar: DEFAULT_AVATARS[0],
  isOnline: true,
  statusText: "Đang hoạt động",
  hasVerifiedBadge: false,
  themeKey: "classic",
  isDarkMode: false,

  // iOS System Bar controls
  currentTime: "09:41",
  batteryLevel: 92,
  isCharging: false,
  signalBars: 4,
  wifiEnabled: true,
  cellularType: "5G",
  showIosStatusBar: true,
  showHomeBar: true,

  // App mode & interaction
  activeSender: "me", // "me" | "them"
  isSnapshotMode: false,
  activeModal: null, // null | 'profile' | 'edit_message' | 'attach' | 'call' | 'presets'
  editingMessageId: null,
  callType: "audio", // "audio" | "video"
  callStatus: "incoming", // "incoming" | "connected"
  callTimer: 0,

  // Chat message list
  messages: [
    {
      id: "m-1",
      sender: "them",
      type: "text",
      content: "Chào anh, hôm nay anh có rảnh đi cafe không ạ? ✨",
      timestamp: "09:30",
      status: "seen"
    },
    {
      id: "m-2",
      sender: "me",
      type: "text",
      content: "Anh rảnh nè, hẹn em 10h ở quán quen nhé! ☕",
      timestamp: "09:32",
      status: "seen"
    },
    {
      id: "m-3",
      sender: "them",
      type: "voice",
      content: "",
      voiceDuration: "0:14",
      timestamp: "09:33",
      status: "seen"
    },
    {
      id: "m-4",
      sender: "me",
      type: "like",
      content: "👍",
      timestamp: "09:35",
      status: "seen"
    },
    {
      id: "m-5",
      sender: "them",
      type: "text",
      content: "Dạ vâng, em đang chuẩn bị xuất phát rồi nè ❤️",
      timestamp: "09:38",
      status: "seen"
    }
  ]
});

// Helper actions
export function addMessage(data) {
  const newMsg = {
    id: "m-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
    sender: data.sender || chatState.activeSender,
    type: data.type || "text",
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || (data.sender === "me" ? "delivered" : "seen"),
    voiceDuration: data.voiceDuration || "0:15",
    imageUri: data.imageUri || null,
    callInfo: data.callInfo || null
  };
  chatState.messages.push(newMsg);
}

export function updateMessage(id, updates) {
  const index = chatState.messages.findIndex(m => m.id === id);
  if (index !== -1) {
    chatState.messages[index] = { ...chatState.messages[index], ...updates };
  }
}

export function deleteMessage(id) {
  chatState.messages = chatState.messages.filter(m => m.id !== id);
}

export function insertMessageAt(id, data, position = "after") {
  const index = chatState.messages.findIndex(m => m.id === id);
  if (index === -1) return;
  const newMsg = {
    id: "m-" + Date.now(),
    sender: data.sender || chatState.activeSender,
    type: data.type || "text",
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || "seen"
  };
  if (position === "after") {
    chatState.messages.splice(index + 1, 0, newMsg);
  } else {
    chatState.messages.splice(index, 0, newMsg);
  }
}

export function clearAllMessages() {
  chatState.messages = [];
}

export function getCurrentFormattedTime() {
  const d = new Date();
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
}

