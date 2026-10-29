// Svelte 5 Reactive State Store for Fake Chat Messenger & Zalo - Exact 1:1 Clone

export const DEFAULT_AVATARS = [
  "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=faces",
  "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces"
];

/** @type {Record<string, { id: string, name: string, primary: string, bgRight: string, textRight: string }>} */
export const THEMES = {
  classic: {
    id: "classic",
    name: "Classic Blue",
    primary: "#0084FF",
    bgRight: "bg-[#0084FF]",
    textRight: "text-white"
  },
  ocean: {
    id: "ocean",
    name: "Ocean Purple",
    primary: "#7B37FF",
    bgRight: "bg-[#7B37FF]",
    textRight: "text-white"
  },
  berry: {
    id: "berry",
    name: "Berry Pink",
    primary: "#FF2A6D",
    bgRight: "bg-[#FF2A6D]",
    textRight: "text-white"
  },
  sunset: {
    id: "sunset",
    name: "Sunset Peach",
    primary: "#FA709A",
    bgRight: "bg-[#FA709A]",
    textRight: "text-white"
  }
};

export const chatState = $state({
  // App Switcher: 'messenger' | 'zalo'
  currentApp: 'messenger',

  // Navigation Screens for Messenger: 'chats_list' | 'chat_room' | 'create_contact'
  currentScreen: 'chat_room',
  activeNavTab: 'chats',

  // Navigation Screens for Zalo: 'zalo_chats_list' | 'zalo_chat_room' | 'zalo_create_contact'
  zaloScreen: 'zalo_chat_room',
  zaloActiveTab: 'messages',
  zaloActiveContactId: 'z-1',

  // App Theme & Mode
  isDarkMode: false,
  isSnapshotMode: false,
  /** @type {string | null} */
  activeModal: null, // null | 'profile' | 'edit_message' | 'attach' | 'call' | 'react' | 'message_action'
  /** @type {string | null} */
  editingMessageId: null,
  /** @type {string | null} */
  reactingMessageId: null,
  /** @type {any} */
  selectedActionMessage: null,
  /** @type {any} */
  replyingToMessage: null,

  // Active Conversation Info (selected or default)
  activeContactId: "c-1",

  // Contacts / Conversations List for Messenger (All demo messages emptied as requested)
  conversations: [
    {
      id: "c-1",
      name: "Trịnh Văn Mạnh",
      avatar: DEFAULT_AVATARS[0],
      isOnline: true,
      statusText: "Đang hoạt động",
      hasVerifiedBadge: false,
      themeKey: "classic",
      unreadCount: 0,
      lastMessage: "",
      lastTime: "Vừa xong",
      messages: []
    },
    {
      id: "c-2",
      name: "Nguyễn Thảo My",
      avatar: DEFAULT_AVATARS[1],
      isOnline: true,
      statusText: "Hoạt động 5 phút trước",
      hasVerifiedBadge: true,
      themeKey: "ocean",
      unreadCount: 0,
      lastMessage: "",
      lastTime: "08:15",
      messages: []
    },
    {
      id: "c-3",
      name: "Đức Nguyễn",
      avatar: DEFAULT_AVATARS[2],
      isOnline: false,
      statusText: "Hoạt động 1 giờ trước",
      hasVerifiedBadge: false,
      themeKey: "classic",
      unreadCount: 0,
      lastMessage: "",
      lastTime: "Hôm qua",
      messages: []
    }
  ],

  // iOS System Bar controls
  currentTime: "09:41",
  batteryLevel: 92,
  isCharging: false,
  signalBars: 4,
  wifiEnabled: true,
  cellularType: "5G",
  showIosStatusBar: true,
  showDynamicIsland: false,
  showHomeBar: true,

  // Active sender in current chat: 'me' | 'them'
  activeSender: "me",

  // Zalo Conversations List (All demo messages emptied as requested)
  zaloConversations: [
    {
      id: "z-1",
      name: "Trần Huyền Trang",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&h=300&fit=crop&crop=faces",
      statusText: "Vừa mới truy cập",
      isOnline: true,
      hasVerifiedBadge: false,
      lastMessage: "",
      lastTime: "Vừa xong",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-2",
      name: "Lỗi đổ đầu chúng toi",
      avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      isOnline: false,
      hasVerifiedBadge: false,
      lastMessage: "",
      lastTime: "19/10",
      isPinned: true,
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-3",
      name: "Zalo Bảo Mật",
      avatar: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=300&h=300&fit=crop&crop=faces",
      statusText: "Tài khoản chính thức",
      hasVerifiedBadge: true,
      isOnline: true,
      lastMessage: "",
      lastTime: "6 giờ",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-4",
      name: "Nguyễn Thị Hải Ninh",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop&crop=faces",
      statusText: "Truy cập 15 phút trước",
      hasVerifiedBadge: false,
      isOnline: false,
      lastMessage: "",
      lastTime: "9 giờ",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-5",
      name: "Thiết kế đồ hoạ",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      hasVerifiedBadge: false,
      isOnline: true,
      lastMessage: "",
      lastTime: "22 giờ",
      unreadCount: 0,
      hasMention: true,
      messages: []
    },
    {
      id: "z-6",
      name: "Game Data Research",
      avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      hasVerifiedBadge: false,
      isOnline: true,
      lastMessage: "",
      lastTime: "T3",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-7",
      name: "Quyên Xử Lý Nước",
      avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&h=300&fit=crop&crop=faces",
      statusText: "Truy cập 1 giờ trước",
      hasVerifiedBadge: false,
      isOnline: false,
      lastMessage: "",
      lastTime: "T2",
      unreadCount: 0,
      messages: []
    }
  ],

  // Call simulation
  callType: "audio", // "audio" | "video"
  callStatus: "incoming", // "incoming" | "connected"
  callTimer: 0
});

// Helper getters
export function getActiveConversation() {
  const conv = chatState.conversations.find(c => c.id === chatState.activeContactId);
  return conv || chatState.conversations[0];
}

export function getActiveZaloConversation() {
  const conv = chatState.zaloConversations.find(c => c.id === chatState.zaloActiveContactId);
  return conv || chatState.zaloConversations[0];
}

export function getCurrentActiveChat() {
  return chatState.currentApp === 'zalo' ? getActiveZaloConversation() : getActiveConversation();
}

// Helper actions
export function selectConversation(/** @type {string} */ id) {
  chatState.activeContactId = id;
  chatState.currentScreen = 'chat_room';
}

export function addConversation(/** @type {any} */ data) {
  const newId = "c-" + Date.now();
  const newConv = {
    id: newId,
    name: data.name || "Người liên hệ mới",
    avatar: data.avatar || DEFAULT_AVATARS[0],
    isOnline: data.isOnline !== undefined ? data.isOnline : true,
    statusText: data.statusText || "Đang hoạt động",
    hasVerifiedBadge: data.hasVerifiedBadge || false,
    themeKey: data.themeKey || "classic",
    unreadCount: data.unreadCount || 0,
    lastMessage: "",
    lastTime: getCurrentFormattedTime(),
    messages: []
  };
  chatState.conversations.unshift(newConv);
  chatState.activeContactId = newId;
  chatState.currentScreen = 'chat_room';
}

export function addMessage(/** @type {any} */ data) {
  const conv = getActiveConversation();
  const quote = chatState.replyingToMessage;
  const newMsg = {
    id: "m-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
    sender: data.sender || chatState.activeSender,
    type: data.type || "text",
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || (data.sender === "me" ? "delivered" : "seen"),
    voiceDuration: data.voiceDuration || "0:15",
    imageUri: data.imageUri || null,
    callInfo: data.callInfo || null,
    quoteSender: quote ? (quote.sender === 'me' ? 'Bạn' : conv.name) : (data.quoteSender || null),
    quoteText: quote ? (quote.content || (quote.type === 'voice' ? 'Tin nhắn thoại' : 'Hình ảnh')) : (data.quoteText || null),
    react: null
  };
  conv.messages.push(newMsg);
  conv.lastMessage = data.type === 'like' ? '👍' : (data.content || 'Đã gửi file');
  conv.lastTime = newMsg.timestamp;
  chatState.replyingToMessage = null; // Clear reply after sending
}

export function updateMessage(/** @type {string} */ id, /** @type {any} */ updates) {
  const conv = getCurrentActiveChat();
  const index = conv.messages.findIndex(m => m.id === id);
  if (index !== -1) {
    conv.messages[index] = { ...conv.messages[index], ...updates };
  }
}

export function deleteMessage(/** @type {string} */ id) {
  const conv = getCurrentActiveChat();
  conv.messages = conv.messages.filter(m => m.id !== id);
}

export function insertMessageAt(/** @type {string} */ id, /** @type {any} */ data, position = "after") {
  const conv = getCurrentActiveChat();
  const index = conv.messages.findIndex(m => m.id === id);
  if (index === -1) return;
  const newMsg = {
    id: "m-" + Date.now(),
    sender: data.sender || chatState.activeSender,
    type: data.type || "text",
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || "seen",
    react: null
  };
  if (position === "after") {
    conv.messages.splice(index + 1, 0, newMsg);
  } else {
    conv.messages.splice(index, 0, newMsg);
  }
}

export function toggleMessageSender(/** @type {string} */ id) {
  const conv = getCurrentActiveChat();
  const msg = conv.messages.find(m => m.id === id);
  if (msg) {
    msg.sender = msg.sender === 'me' ? 'them' : 'me';
  }
}

export function setReaction(/** @type {string} */ msgId, /** @type {string | null} */ reactType) {
  const conv = getCurrentActiveChat();
  const msg = conv.messages.find(m => m.id === msgId);
  if (msg) {
    if (chatState.currentApp === 'zalo') {
      msg.hasHeart = !msg.hasHeart;
    } else {
      msg.react = msg.react === reactType ? null : reactType;
    }
  }
  chatState.activeModal = null;
  chatState.reactingMessageId = null;
  chatState.selectedActionMessage = null;
}

export function clearCurrentChat() {
  const conv = getCurrentActiveChat();
  if (conv) {
    conv.messages = [];
    conv.lastMessage = "";
  }
}

export const clearAllMessages = clearCurrentChat;

// --- ZALO HELPERS ---
export function selectZaloConversation(/** @type {string} */ id) {
  chatState.zaloActiveContactId = id;
  chatState.zaloScreen = 'zalo_chat_room';
}

export function addZaloConversation(/** @type {any} */ data) {
  const newId = "z-" + Date.now();
  const newConv = {
    id: newId,
    name: data.name || "Người liên hệ Zalo mới",
    avatar: data.avatar || DEFAULT_AVATARS[0],
    isOnline: data.isOnline !== undefined ? data.isOnline : true,
    statusText: data.statusText || "Vừa mới truy cập",
    hasVerifiedBadge: data.hasVerifiedBadge || false,
    unreadCount: data.unreadCount || 0,
    isPinned: data.isPinned || false,
    lastMessage: "",
    lastTime: getCurrentFormattedTime(),
    messages: []
  };
  chatState.zaloConversations.unshift(newConv);
  chatState.zaloActiveContactId = newId;
  chatState.zaloScreen = 'zalo_chat_room';
}

export function addZaloMessage(/** @type {any} */ data) {
  const conv = getActiveZaloConversation();
  const quote = chatState.replyingToMessage;
  const isQuote = !!quote || !!data.quoteText;
  const newMsg = {
    id: "zm-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
    sender: data.sender || chatState.activeSender,
    type: isQuote ? 'reply_quote' : (data.type || "text"),
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || (data.sender === "me" ? "received" : "seen"),
    hasHeart: data.hasHeart || false,
    cardName: data.cardName || null,
    cardAvatar: data.cardAvatar || null,
    quoteSender: quote ? (quote.sender === 'me' ? 'Bạn' : conv.name) : (data.quoteSender || null),
    quoteText: quote ? (quote.content || (quote.type === 'voice' ? 'Tin nhắn thoại' : 'Hình ảnh')) : (data.quoteText || null),
    imageUri: data.imageUri || null,
    voiceDuration: data.voiceDuration || "0:15"
  };
  conv.messages.push(newMsg);
  conv.lastMessage = data.content || "Đã gửi file";
  conv.lastTime = newMsg.timestamp;
  chatState.replyingToMessage = null; // Clear reply after sending
}

export function toggleZaloHeart(/** @type {string} */ msgId) {
  const conv = getActiveZaloConversation();
  const msg = conv.messages.find(m => m.id === msgId);
  if (msg) {
    msg.hasHeart = !msg.hasHeart;
  }
}

export function deleteZaloMessage(/** @type {string} */ msgId) {
  const conv = getActiveZaloConversation();
  conv.messages = conv.messages.filter(m => m.id !== msgId);
}

export function getCurrentFormattedTime() {
  const d = new Date();
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  return `${hours}:${minutes}`;
}
