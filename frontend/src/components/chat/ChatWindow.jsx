import React, { useRef, useEffect, useState } from 'react';
import { useChat } from '../../store/chatStore';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatSessionSidebar from './ChatSessionSidebar';
import { RotateCcw, Bot, Shield, PanelLeftClose, PanelLeft, Plus, History } from 'lucide-react';

export default function ChatWindow() {
  const {
    messages,
    sessions,
    currentSessionId,
    isLoading,
    error,
    sendMessage,
    confirmAction,
    createNewSession,
    selectSession,
    deleteSession,
    clearChat
  } = useChat();

  const [sidebarOpen, setSidebarOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const activeSession = sessions.find(s => s.session_id === currentSessionId);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  return (
    <div className="flex h-[calc(100vh-4rem)] bg-slate-50 overflow-hidden">
      {/* Sessions History Sidebar */}
      <ChatSessionSidebar
        sessions={sessions}
        currentSessionId={currentSessionId}
        onSelectSession={selectSession}
        onCreateSession={createNewSession}
        onDeleteSession={deleteSession}
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 h-full">
        {/* Chat Header */}
        <div className="h-14 bg-white border-b border-slate-200 px-4 sm:px-6 flex items-center justify-between flex-shrink-0">
          <div className="flex items-center space-x-3 min-w-0">
            {/* Toggle Sidebar on mobile/desktop */}
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="p-1.5 text-slate-500 hover:text-slate-800 hover:bg-slate-100 rounded-lg transition-colors md:hidden"
              title="Toggle Sessions History"
            >
              <History className="w-4 h-4" />
            </button>

            <div className="flex items-center space-x-2.5 min-w-0">
              <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse flex-shrink-0"></div>
              <div className="min-w-0">
                <span className="font-bold text-slate-800 text-sm truncate block">
                  {activeSession?.title || 'AI Banking Concierge'}
                </span>
                <span className="text-[10px] text-slate-400 block truncate">
                  Session: {currentSessionId || 'Active'} • Multi-turn Memory Enabled
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={() => createNewSession('New Banking Conversation')}
              className="text-xs text-sky-600 hover:text-sky-800 flex items-center space-x-1 px-2.5 py-1 rounded-lg hover:bg-sky-50 transition-colors border border-sky-200"
              title="Start a new conversation"
            >
              <Plus className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">New Chat</span>
            </button>

            <button
              onClick={clearChat}
              className="text-xs text-slate-500 hover:text-slate-800 flex items-center space-x-1.5 px-2.5 py-1 rounded-lg hover:bg-slate-100 transition-colors"
              title="Reset current conversation"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">Reset</span>
            </button>
          </div>
        </div>

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400 space-y-2">
              <Bot className="w-10 h-10 text-slate-300 animate-bounce" />
              <p className="text-sm font-medium text-slate-600">Start a banking conversation</p>
              <p className="text-xs max-w-sm">
                Ask about account balances, card controls, upcoming bills, loan eligibility, or report suspicious charges.
              </p>
            </div>
          ) : (
            messages.map((msg) => (
              <ChatMessage
                key={msg.id}
                message={msg}
                onConfirmAction={confirmAction}
              />
            ))
          )}

          {isLoading && (
            <div className="flex items-start space-x-3">
              <div className="w-8 h-8 rounded-full bg-slate-200 text-slate-500 flex items-center justify-center animate-pulse">
                <Bot className="w-4 h-4" />
              </div>
              <div className="bg-white border border-slate-200 p-3.5 rounded-2xl rounded-tl-none shadow-sm flex items-center space-x-2 text-xs text-slate-500">
                <div className="w-2 h-2 rounded-full bg-sky-500 animate-bounce"></div>
                <div className="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:0.2s]"></div>
                <div className="w-2 h-2 rounded-full bg-sky-500 animate-bounce [animation-delay:0.4s]"></div>
                <span className="pl-1">Executing deterministic banking tools & AI synthesis...</span>
              </div>
            </div>
          )}

          {error && (
            <div className="p-3 bg-rose-50 border border-rose-200 text-rose-700 text-xs rounded-xl">
              {error}
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
}
