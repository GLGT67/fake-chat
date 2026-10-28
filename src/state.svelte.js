// Svelte 5 Reactive State Store for Fake Chat Messenger - Exact 1:1 APK Clone

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
  zaloActiveTab: 'messages', // 'messages' | 'contacts' | 'explore' | 'timeline' | 'profile'
  zaloActiveContactId: 'z-1',

  // App Theme & Mode
  isDarkMode: false,
  isSnapshotMode: false,
  /** @type {string | null} */
  activeModal: null, // null | 'profile' | 'edit_message' | 'attach' | 'call' | 'react'
  /** @type {string | null} */
  editingMessageId: null,
  /** @type {string | null} */
  reactingMessageId: null,

  // Active Conversation Info (selected or default)
  activeContactId: "c-1",

  get partnerName() {
    const c = this.conversations.find((/** @type {any} */ item) => item.id === this.activeContactId);
    return (c || this.conversations[0])?.name || "";
  },
  get partnerAvatar() {
    const c = this.conversations.find((/** @type {any} */ item) => item.id === this.activeContactId);
    return (c || this.conversations[0])?.avatar || "";
  },

  // Contacts / Conversations List (100% like activity_main_messenger)
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
      lastMessage: "Dạ vâng, em đang chuẩn bị xuất phát rồi nè ❤️",
      lastTime: "09:38",
      messages: [
        {
          id: "m-1",
          sender: "them",
          type: "text",
          content: "Chào anh, hôm nay anh có rảnh đi cafe không ạ? ✨",
          timestamp: "09:30",
          status: "seen",
          react: null
        },
        {
          id: "m-2",
          sender: "me",
          type: "text",
          content: "Anh rảnh nè, hẹn em 10h ở quán quen nhé! ☕",
          timestamp: "09:32",
          status: "seen",
          react: "heart"
        },
        {
          id: "m-3",
          sender: "them",
          type: "voice",
          content: "",
          voiceDuration: "0:14",
          timestamp: "09:33",
          status: "seen",
          react: null
        },
        {
          id: "m-4",
          sender: "me",
          type: "like",
          content: "👍",
          timestamp: "09:35",
          status: "seen",
          react: null
        },
        {
          id: "m-5",
          sender: "them",
          type: "text",
          content: "Dạ vâng, em đang chuẩn bị xuất phát rồi nè ❤️",
          timestamp: "09:38",
          status: "seen",
          react: "like"
        }
      ]
    },
    {
      id: "c-2",
      name: "Nguyễn Thảo My",
      avatar: DEFAULT_AVATARS[1],
      isOnline: true,
      statusText: "Hoạt động 5 phút trước",
      hasVerifiedBadge: true,
      themeKey: "ocean",
      unreadCount: 2,
      lastMessage: "Tối nay nhớ gọi cho em nhé!",
      lastTime: "08:15",
      messages: [
        {
          id: "m-201",
          sender: "them",
          type: "text",
          content: "Tối nay nhớ gọi cho em nhé!",
          timestamp: "08:15",
          status: "seen",
          react: null
        }
      ]
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
      lastMessage: "Hôm nay gửi file báo cáo cho mình nhé.",
      lastTime: "Hôm qua",
      messages: [
        {
          id: "m-301",
          sender: "them",
          type: "text",
          content: "Hôm nay gửi file báo cáo cho mình nhé.",
          timestamp: "Hôm qua",
          status: "seen",
          react: null
        }
      ]
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
  showDynamicIsland: false, // Tắt theo mặc định để ảnh chụp màn hình sạch 100% như ảnh chụp phím cứng iPhone
  showHomeBar: true,

  // Active sender in current chat: 'me' | 'them'
  activeSender: "me",

  // Zalo Conversations List (100% like sample images)
  zaloConversations: [
    {
      id: "z-1",
      name: "Trần Huyền Trang",
      avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&h=300&fit=crop&crop=faces",
      statusText: "Vừa mới truy cập",
      isOnline: true,
      lastMessage: "dạ em mới gửi kb rồi",
      lastTime: "16:56",
      unreadCount: 0,
      messages: [
        {
          id: "zm-1",
          sender: "them",
          type: "text",
          content: "Mấy studio lớn thì nó tách ra thành 1 bộ phận khác luôn là UA",
          timestamp: "16:33",
          status: "seen",
          hasHeart: false
        },
        {
          id: "zm-2",
          sender: "me",
          type: "text",
          content: "dạ",
          timestamp: "16:51",
          status: "seen",
          hasHeart: false
        },
        {
          id: "zm-3",
          sender: "me",
          type: "text",
          content: "thế cho em ứng ạ",
          timestamp: "16:51",
          status: "seen",
          hasHeart: false
        },
        {
          id: "zm-4",
          sender: "me",
          type: "text",
          content: "=))",
          timestamp: "16:52",
          status: "seen",
          hasHeart: false
        },
        {
          id: "zm-5",
          sender: "them",
          type: "contact_card",
          cardName: "Thu Hướng",
          cardAvatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces",
          content: "Danh thiếp Zalo",
          timestamp: "16:55",
          status: "seen",
          hasHeart: true
        },
        {
          id: "zm-6",
          sender: "them",
          type: "reply_quote",
          quoteSender: "Nguyễn sơn Tùng",
          quoteText: "thế cho em ứng ạ",
          content: "Nhắn i",
          timestamp: "16:56",
          status: "seen",
          hasHeart: true
        },
        {
          id: "zm-7",
          sender: "me",
          type: "text",
          content: "dạ em mới gửi kb rồi",
          timestamp: "16:56",
          status: "received",
          hasHeart: false
        }
      ]
    },
    {
      id: "z-2",
      name: "Lỗi đổ đầu chúng toi",
      avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      isOnline: false,
      lastMessage: "Thuý yêu: 2 giám khảo",
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
      lastMessage: "Xác nhận hành vi bất thường trên tài...",
      lastTime: "6 giờ",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-4",
      name: "Nguyễn Thị Hải Ninh",
      avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=300&h=300&fit=crop&crop=faces",
      statusText: "Truy cập 15 phút trước",
      isOnline: false,
      lastMessage: "Ok",
      lastTime: "9 giờ",
      unreadCount: 1,
      messages: []
    },
    {
      id: "z-5",
      name: "Thiết kế đồ hoạ - B25GA04_D...",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      isOnline: true,
      lastMessage: "Phan Thu Trang: @All mng gửi...",
      lastTime: "22 giờ",
      unreadCount: 2,
      hasMention: true,
      messages: []
    },
    {
      id: "z-6",
      name: "Game Data Research",
      avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=300&h=300&fit=crop&crop=faces",
      statusText: "",
      isOnline: true,
      lastMessage: "Thu Hương: không bôi đậm bừa bãi nhé",
      lastTime: "T3",
      unreadCount: 0,
      messages: []
    },
    {
      id: "z-7",
      name: "Quyên Xử Lý Nước",
      avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&h=300&fit=crop&crop=faces",
      statusText: "Truy cập 1 giờ trước",
      isOnline: false,
      lastMessage: "[Cuộc gọi thoại nhỡ]",
      lastTime: "T2",
      unreadCount: 1,
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
    lastMessage: data.lastMessage || "Xin chào!",
    lastTime: getCurrentFormattedTime(),
    messages: [
      {
        id: "m-" + Date.now(),
        sender: "them",
        type: "text",
        content: data.lastMessage || "Xin chào!",
        timestamp: getCurrentFormattedTime(),
        status: "seen",
        react: null
      }
    ]
  };
  chatState.conversations.unshift(newConv);
  chatState.activeContactId = newId;
  chatState.currentScreen = 'chat_room';
}

export function addMessage(/** @type {any} */ data) {
  const conv = getActiveConversation();
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
    react: null
  };
  conv.messages.push(newMsg);
  conv.lastMessage = data.type === 'like' ? '👍' : (data.content || 'Đã gửi file');
  conv.lastTime = newMsg.timestamp;
}

export function updateMessage(/** @type {string} */ id, /** @type {any} */ updates) {
  const conv = getActiveConversation();
  const index = conv.messages.findIndex(m => m.id === id);
  if (index !== -1) {
    conv.messages[index] = { ...conv.messages[index], ...updates };
  }
}

export function deleteMessage(/** @type {string} */ id) {
  const conv = getActiveConversation();
  conv.messages = conv.messages.filter(m => m.id !== id);
}

export function insertMessageAt(/** @type {string} */ id, /** @type {any} */ data, position = "after") {
  const conv = getActiveConversation();
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

export function setReaction(/** @type {string} */ msgId, /** @type {string | null} */ reactType) {
  const conv = getActiveConversation();
  const msg = conv.messages.find(m => m.id === msgId);
  if (msg) {
    msg.react = msg.react === reactType ? null : reactType;
  }
  chatState.activeModal = null;
  chatState.reactingMessageId = null;
}

export function clearCurrentChat() {
  const conv = getActiveConversation();
  conv.messages = [];
  conv.lastMessage = "";
}

export const clearAllMessages = clearCurrentChat;

// --- ZALO HELPERS ---
export function getActiveZaloConversation() {
  const conv = chatState.zaloConversations.find(c => c.id === chatState.zaloActiveContactId);
  return conv || chatState.zaloConversations[0];
}

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
    lastMessage: data.lastMessage || "Xin chào bạn!",
    lastTime: getCurrentFormattedTime(),
    messages: [
      {
        id: "zm-" + Date.now(),
        sender: "them",
        type: "text",
        content: data.lastMessage || "Xin chào bạn!",
        timestamp: getCurrentFormattedTime(),
        status: "seen",
        hasHeart: false
      }
    ]
  };
  chatState.zaloConversations.unshift(newConv);
  chatState.zaloActiveContactId = newId;
  chatState.zaloScreen = 'zalo_chat_room';
}

export function addZaloMessage(/** @type {any} */ data) {
  const conv = getActiveZaloConversation();
  const newMsg = {
    id: "zm-" + Date.now() + "-" + Math.random().toString(36).substr(2, 4),
    sender: data.sender || chatState.activeSender,
    type: data.type || "text",
    content: data.content || "",
    timestamp: data.timestamp || getCurrentFormattedTime(),
    status: data.status || (data.sender === "me" ? "received" : "seen"),
    hasHeart: data.hasHeart || false,
    cardName: data.cardName || null,
    cardAvatar: data.cardAvatar || null,
    quoteSender: data.quoteSender || null,
    quoteText: data.quoteText || null,
    imageUri: data.imageUri || null,
    voiceDuration: data.voiceDuration || "0:15"
  };
  conv.messages.push(newMsg);
  conv.lastMessage = data.content || "Đã gửi file";
  conv.lastTime = newMsg.timestamp;
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
