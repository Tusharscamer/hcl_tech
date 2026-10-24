import React from 'react';
import { Plus, MessageSquare, Trash2, Clock, ChevronRight } from 'lucide-react';

export default function ChatSessionSidebar({
  sessions,
  currentSessionId,
  onSelectSession,
  onCreateSession,
  onDeleteSession,
  isOpen,
  onClose
}) {
  return (
    <div
      className={`
        ${isOpen ? 'w-72' : 'w-0 sm:w-16 md:w-72'} 
        transition-all duration-200 ease-in-out
        bg-white border-r border-slate-200 flex flex-col h-full overflow-hidden flex-shrink-0
      `}
    >
      {/* Top Header & New Chat Button */}
      <div className="p-3 border-b border-slate-100 flex items-center justify-between gap-2">
        <button
          onClick={() => onCreateSession('New Banking Conversation')}
          className="flex-1 flex items-center justify-center space-x-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white px-3 py-2 rounded-xl text-xs font-semibold shadow-sm transition-all"
          title="Create New Conversation"
        >
          <Plus className="w-4 h-4 flex-shrink-0" />
          <span className="hidden md:inline truncate">New Banking Chat</span>
        </button>
      </div>

      {/* Sessions List */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        <div className="px-2 py-1 text-[11px] font-bold text-slate-400 uppercase tracking-wider hidden md:block">
          Recent Sessions ({sessions.length})
        </div>

        {sessions.length === 0 ? (
          <div className="p-4 text-center text-xs text-slate-400">
            No previous sessions
          </div>
        ) : (
          sessions.map((sess) => {
            const isActive = sess.session_id === currentSessionId;
            const updatedDate = sess.updated_at
              ? new Date(sess.updated_at).toLocaleDateString([], { month: 'short', day: 'numeric' })
              : 'Today';

            return (
              <div
                key={sess.session_id}
                onClick={() => onSelectSession(sess.session_id)}
                className={`
                  group relative flex items-center justify-between px-3 py-2.5 rounded-xl cursor-pointer text-xs transition-colors
                  ${isActive 
                    ? 'bg-sky-50 text-sky-900 border border-sky-200 font-medium shadow-xs' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'}
                `}
                title={sess.title}
              >
                <div className="flex items-center space-x-2.5 min-w-0 flex-1">
                  <MessageSquare className={`w-4 h-4 flex-shrink-0 ${isActive ? 'text-sky-600' : 'text-slate-400 group-hover:text-slate-600'}`} />
                  <div className="min-w-0 flex-1 hidden md:block">
                    <p className="truncate font-medium text-slate-800 leading-tight">
                      {sess.title || 'Banking Conversation'}
                    </p>
                    <div className="flex items-center space-x-2 text-[10px] text-slate-400 mt-0.5">
                      <span>{updatedDate}</span>
                      <span>•</span>
                      <span>{sess.message_count || 1} msgs</span>
                    </div>
                  </div>
                </div>

                {/* Delete Session Button */}
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    if (confirm('Delete this conversation session?')) {
                      onDeleteSession(sess.session_id);
                    }
                  }}
                  title="Delete Session"
                  className="opacity-0 group-hover:opacity-100 p-1 hover:text-rose-600 hover:bg-rose-50 rounded-md transition-opacity hidden md:block"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                </button>
              </div>
            );
          })
        )}
      </div>

      {/* Footer Info */}
      <div className="p-3 bg-slate-50 border-t border-slate-200 text-[11px] text-slate-400 hidden md:flex items-center justify-between">
        <span className="flex items-center space-x-1">
          <Clock className="w-3 h-3" />
          <span>Multi-turn Memory Active</span>
        </span>
      </div>
    </div>
  );
}
