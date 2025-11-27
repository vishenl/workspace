# Six App: GetStream Feature Implementation Guide

## Executive Summary

This document provides a comprehensive roadmap for enhancing the Six social/community app using GetStream's platform. Since Six already has chat and feeds implemented, this guide focuses on **high-impact features** that will accelerate development and create a best-in-class user experience.

**Priority**: Features are ranked by implementation value (⭐⭐⭐ = Critical, ⭐⭐ = High Priority, ⭐ = Nice to Have)

---

## Phase 1: Core Chat Enhancements (Week 1-2)

### 1. Message Reactions ⭐⭐⭐

**Why**: Essential for engagement and emotional expression in a social app.

**Installation**: Already included in `stream-chat-react`

**Implementation**:

```javascript
import {
  Channel,
  MessageList,
  ReactionSelector,
  ReactionsList
} from 'stream-chat-react';

// Enable reactions in your channel
<Channel ReactionSelector={ReactionSelector} reactionOptions={defaultReactionOptions}>
  <MessageList />
</Channel>
```

**Custom Reactions**:

```javascript
import { MessageList } from 'stream-chat-react';

const customReactionOptions = [
  { type: 'love', Component: LoveIcon },
  { type: 'fire', Component: FireIcon },
  { type: 'celebrate', Component: CelebrateIcon },
  { type: 'thinking', Component: ThinkingIcon },
];

<Channel reactionOptions={customReactionOptions}>
  <MessageList />
</Channel>
```

**API Usage**:

```javascript
// Add a reaction
await channel.sendReaction(messageId, { type: 'love' });

// Remove a reaction
await channel.deleteReaction(messageId, 'love');

// Get reactions
const { reactions } = message;
```

**Resources**:
- [Reactions Documentation](https://getstream.io/chat/docs/sdk/react/components/message-components/reactions/)
- [Send Reaction API](https://getstream.io/chat/docs/react/send_reaction/)

---

### 2. Threaded Conversations ⭐⭐⭐

**Why**: Keeps conversations organized, reduces noise, and improves discussion quality.

**Implementation**:

```javascript
import { Channel, Thread, MessageList } from 'stream-chat-react';

<Channel>
  <Window>
    <MessageList />
    <MessageInput />
  </Window>
  <Thread /> {/* Renders when user clicks "Reply in Thread" */}
</Channel>
```

**Creating a Thread**:

```javascript
// Send a threaded reply
await channel.sendMessage({
  text: 'This is a reply',
  parent_id: parentMessageId, // ID of the message being replied to
});
```

**Custom Thread Behavior**:

```javascript
import { useOpenThreadHandler } from 'stream-chat-react';

const CustomMessage = (props) => {
  const handleOpenThread = useOpenThreadHandler(props.message);

  return (
    <div onClick={handleOpenThread}>
      {props.message.text}
      {props.message.reply_count > 0 && (
        <span>{props.message.reply_count} replies</span>
      )}
    </div>
  );
};
```

**Resources**:
- [Threading Documentation](https://getstream.io/chat/docs/react/threads/)
- [Message Hooks](https://getstream.io/chat/docs/sdk/react/hooks/message_hooks/)

---

### 3. Pinned Messages ⭐⭐

**Why**: Highlight important announcements, events, or community guidelines.

**Implementation**:

```javascript
// Pin a message
await channel.pinMessage(message, {
  user_id: currentUser.id,
  expires: null, // null = no expiration, or use ISO date string
});

// Unpin a message
await channel.unpinMessage(message);

// Send a new message as pinned
await channel.sendMessage({
  text: 'Important announcement!',
  pinned: true,
  pin_expires: '2025-12-31T23:59:59Z', // Optional expiration
});
```

**Display Pinned Messages**:

```javascript
import { usePinnedMessages } from 'stream-chat-react';

const PinnedMessagesBar = () => {
  const pinnedMessages = usePinnedMessages();

  if (!pinnedMessages?.length) return null;

  return (
    <div className="pinned-messages-bar">
      {pinnedMessages.map(msg => (
        <div key={msg.id} className="pinned-message">
          📌 {msg.text}
        </div>
      ))}
    </div>
  );
};
```

**Resources**:
- [Pinned Messages Documentation](https://getstream.io/chat/docs/react/pinned_messages/)

---

### 4. User Presence & Typing Indicators ⭐⭐⭐

**Why**: Shows who's online and actively engaged, increasing perceived activity.

**Implementation** (mostly automatic):

```javascript
import { ChannelList } from 'stream-chat-react';

// Enable presence in channel list
<ChannelList
  options={{
    presence: true,  // Enable presence tracking
    state: true,     // Sync channel state
    watch: true,     // Watch for real-time updates
  }}
/>
```

**Custom Presence Indicators**:

```javascript
import { Avatar } from 'stream-chat-react';

const CustomAvatar = ({ user }) => {
  const isOnline = user.online;

  return (
    <div className="avatar-container">
      <Avatar image={user.image} name={user.name} />
      {isOnline && <div className="online-indicator" />}
    </div>
  );
};
```

**Typing Indicators** (automatic with MessageInput):

```javascript
// Already enabled by default in MessageInput
// To customize:
import { TypingIndicator } from 'stream-chat-react';

<Channel>
  <MessageList TypingIndicator={CustomTypingIndicator} />
</Channel>
```

---

### 5. Message Search ⭐⭐

**Why**: Critical for finding past conversations and content in a growing community.

**Implementation**:

```javascript
// Search messages across channels
const results = await client.search(
  {
    type: 'messaging',
    members: { $in: [currentUserId] }
  },
  'search query',
  { limit: 25, offset: 0 }
);

// Search within a specific channel
const channelResults = await channel.search('search query', {
  limit: 25,
  offset: 0
});
```

**Search UI Component**:

```javascript
import { SearchBar, SearchResults } from 'stream-chat-react';
import { useState } from 'react';

const MessageSearch = () => {
  const [searchResults, setSearchResults] = useState([]);
  const [query, setQuery] = useState('');

  const handleSearch = async (searchQuery) => {
    setQuery(searchQuery);
    const results = await client.search(
      { members: { $in: [currentUserId] } },
      searchQuery,
      { limit: 25 }
    );
    setSearchResults(results.results);
  };

  return (
    <div>
      <SearchBar onSearch={handleSearch} />
      <SearchResults results={searchResults} />
    </div>
  );
};
```

---

## Phase 2: Advanced Social Features (Week 3-4)

### 6. Activity Feeds - "For You" Personalized Feed ⭐⭐⭐

**Why**: Content discovery drives engagement. The new 2025 API includes AI-powered personalization.

**Installation**:

```bash
npm install getstream
```

**Setup**:

```javascript
import { connect } from 'getstream';

const client = connect(
  'api_key',
  'user_token',
  'app_id'
);

// Get user's feed
const userFeed = client.feed('user', userId);

// Get timeline feed (aggregated from followed users)
const timelineFeed = client.feed('timeline', userId);
```

**Creating Activities**:

```javascript
// Post a new activity
await userFeed.addActivity({
  actor: client.currentUser,
  verb: 'post',
  object: 'post:123',
  content: 'Just shared an amazing moment!',
  image: 'https://...',
  foreign_id: 'post:123',
  time: new Date().toISOString(),
});

// Follow another user
await timelineFeed.follow('user', otherUserId);
```

**Reading Feeds**:

```javascript
// Get activities
const response = await timelineFeed.get({
  limit: 25,
  offset: 0,
  reactions: { recent: true, counts: true }
});

// Activities with reactions
response.results.forEach(activity => {
  console.log(activity.reaction_counts); // { like: 5, comment: 2 }
  console.log(activity.latest_reactions); // Recent reactions
});
```

**Reactions on Activities**:

```javascript
// Like an activity
await client.reactions.add('like', activityId, { userId });

// Comment on an activity
await client.reactions.add('comment', activityId, {
  userId,
  data: { text: 'Great post!' }
});

// Get reactions
const reactions = await client.reactions.filter({
  activity_id: activityId,
  kind: 'like'
});
```

---

### 7. Stories (Ephemeral Content) ⭐⭐

**Why**: Engaging format for casual sharing; drives daily active usage.

**Implementation with Activity Feeds**:

```javascript
// Create a story feed type
const storyFeed = client.feed('story', userId);

// Post a story
await storyFeed.addActivity({
  actor: client.currentUser,
  verb: 'story',
  object: 'story:xyz',
  media: 'https://...',
  expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // 24h
});

// Get active stories
const stories = await storyFeed.get({
  limit: 50,
  enrich: true,
  reactions: { recent: true }
});

// Filter out expired stories
const activeStories = stories.results.filter(story => {
  return new Date(story.expires_at) > new Date();
});
```

---

### 8. Notifications Feed ⭐⭐⭐

**Why**: Keep users informed of interactions and drive re-engagement.

**Setup**:

```javascript
// Create notification feed
const notificationFeed = client.feed('notification', userId);

// Get notifications
const notifications = await notificationFeed.get({
  limit: 25,
  mark_seen: true // Auto-mark as seen
});

// Mark as read
await notificationFeed.get({ mark_read: true });
```

**Notification Types**:

```javascript
// Someone liked your post
await notificationFeed.addActivity({
  actor: likerUserId,
  verb: 'like',
  object: `post:${postId}`,
  target: postAuthorId,
});

// Someone followed you
await notificationFeed.addActivity({
  actor: followerUserId,
  verb: 'follow',
  object: `user:${followedUserId}`,
});

// Someone commented
await notificationFeed.addActivity({
  actor: commenterUserId,
  verb: 'comment',
  object: `post:${postId}`,
  comment_text: 'Nice work!',
});
```

---

### 9. Groups & Forums ⭐⭐

**Why**: Create topic-based communities within Six.

**Implementation**:

```javascript
// Create a group/forum channel
const forumChannel = client.channel('messaging', 'tech-talk', {
  name: 'Tech Talk',
  image: 'https://...',
  topic: 'Discuss all things technology',
  created_by_id: adminUserId,
  members: [userId1, userId2],
  // Custom metadata
  is_forum: true,
  category: 'Technology',
  tags: ['coding', 'startups', 'ai'],
});

await forumChannel.create();
```

**Forum Feed (Activity Feeds)**:

```javascript
// Create a forum-specific feed
const forumFeed = client.feed('forum', forumId);

// Post to forum
await forumFeed.addActivity({
  actor: userId,
  verb: 'post',
  object: `topic:${topicId}`,
  title: 'How do you handle state in React?',
  content: 'I\'m curious about best practices...',
  category: 'Questions',
});
```

---

## Phase 3: Rich Media & AI Features (Week 5-6)

### 10. Video & Audio Calls ⭐⭐⭐

**Why**: Essential for a modern social app; builds deeper connections.

**Installation**:

```bash
npm install @stream-io/video-react-sdk
```

**Setup**:

```javascript
import {
  StreamVideo,
  StreamVideoClient,
  StreamCall,
  useCallStateHooks,
  ParticipantView,
} from '@stream-io/video-react-sdk';

const apiKey = 'your-api-key';
const user = { id: userId, name: userName };
const token = 'user-token';

const videoClient = new StreamVideoClient({ apiKey, user, token });

// Create a 1:1 call
const call = videoClient.call('default', `call-${otherUserId}`);
await call.join({ create: true });

// Video UI Component
const VideoCallUI = () => {
  const { useParticipants } = useCallStateHooks();
  const participants = useParticipants();

  return (
    <StreamVideo client={videoClient}>
      <StreamCall call={call}>
        <div className="video-grid">
          {participants.map((participant) => (
            <ParticipantView
              participant={participant}
              key={participant.sessionId}
            />
          ))}
        </div>
      </StreamCall>
    </StreamVideo>
  );
};
```

**Audio Rooms**:

```javascript
// Create an audio-only room
const audioRoom = videoClient.call('audio_room', 'room-lounge');

await audioRoom.join({
  create: true,
  data: {
    settings_override: {
      video: { enabled: false }, // Audio only
    },
  }
});
```

**Call Controls**:

```javascript
import {
  SpeakerLayout,
  CallControls,
  ToggleAudioButton,
  ToggleVideoButton,
  ScreenShareButton,
} from '@stream-io/video-react-sdk';

const MyCallUI = () => {
  return (
    <StreamCall call={call}>
      <SpeakerLayout />
      <CallControls>
        <ToggleAudioButton />
        <ToggleVideoButton />
        <ScreenShareButton />
      </CallControls>
    </StreamCall>
  );
};
```

---

### 11. Live Streaming ⭐⭐

**Why**: Enable creators to broadcast to their community; drives premium engagement.

**Implementation**:

```javascript
// Create a livestream
const livestream = videoClient.call('livestream', 'stream-id');

await livestream.join({
  create: true,
  data: {
    custom: {
      title: 'Live Q&A Session',
      description: 'Ask me anything!',
    },
  },
});

// Start broadcasting
await livestream.goLive();

// Stop broadcasting
await livestream.stopLive();
```

**Viewer Experience**:

```javascript
// Join as viewer
const viewerCall = videoClient.call('livestream', 'stream-id');
await viewerCall.join();

// React to livestream
await viewerCall.sendReaction({ type: 'love' });
```

**HLS/RTMP Support**:

```javascript
// Get RTMP URL for external encoders (OBS, etc.)
const rtmpUrl = livestream.state.ingress?.rtmp?.address;

// HLS URL for viewers
const hlsUrl = livestream.state.egress?.hls?.playlist_url;
```

---

### 12. AI Chatbot Integration ⭐⭐

**Why**: Provide instant help, recommendations, and engagement 24/7.

**Implementation**:

```javascript
// Create AI assistant channel
const aiChannel = client.channel('messaging', 'ai-assistant', {
  name: 'Six Assistant',
  members: [userId, 'ai-bot'],
});

await aiChannel.create();

// Listen for user messages
client.on('message.new', async (event) => {
  if (event.user.id === 'ai-bot') return; // Don't respond to self

  // Call your AI service (OpenAI, etc.)
  const aiResponse = await generateAIResponse(event.message.text);

  // Send AI response
  await aiChannel.sendMessage({
    text: aiResponse,
    user_id: 'ai-bot',
  });
});
```

**OpenAI Integration Example**:

```javascript
import OpenAI from 'openai';

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function generateAIResponse(userMessage) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: 'You are a helpful assistant for the Six social app.'
      },
      { role: 'user', content: userMessage }
    ],
  });

  return completion.choices[0].message.content;
}
```

---

### 13. AI Content Moderation ⭐⭐⭐

**Why**: Essential for community safety; reduces manual moderation workload by 80%+.

**Setup** (GetStream handles this):

```javascript
// Enable in GetStream Dashboard under Moderation settings
// LLM-powered moderation is enabled by default for new apps

// Custom moderation webhook
const moderationWebhook = async (req, res) => {
  const { message, user } = req.body;

  // GetStream's AI already flagged it
  if (message.moderation_result?.flagged) {
    // Take action: delete, flag for review, etc.
    await channel.deleteMessage(message.id);

    // Or flag for human review
    await addToReviewQueue(message);
  }
};
```

**Custom Moderation Rules**:

```javascript
// Set up in GetStream Dashboard or via API
// Example: Auto-moderate based on toxicity score
const moderationConfig = {
  automod: 'AI',
  automod_behavior: 'flag', // or 'block'
  automod_thresholds: {
    toxicity: 0.7,
    spam: 0.8,
    explicit: 0.6,
  },
};
```

**OCR Image Moderation** (2025 feature):

```javascript
// Automatically moderates text in images
// Enabled in dashboard - no code needed
// Prevents users from bypassing text moderation with screenshots
```

---

## Phase 4: Engagement & Retention (Week 7-8)

### 14. Push Notifications V4 ⭐⭐⭐

**Why**: Critical for re-engagement; new V4 handles 10M+ messages/minute.

**Setup**:

```javascript
// Register device for push notifications
await client.addDevice(deviceToken, 'apn'); // or 'firebase'

// Custom push notification payload
await channel.sendMessage({
  text: 'Check this out!',
  push_notification: {
    title: 'New message from Sarah',
    body: 'Check this out!',
    image: 'https://...',
    badge_count: 5,
  },
});
```

**Smart Grouping** (automatic in V4):

```javascript
// V4 automatically groups notifications
// "Sarah and 3 others sent you messages"
// No additional code needed - enabled by default
```

**User Preferences**:

```javascript
// Let users control notification settings
await client.upsertUser({
  id: userId,
  push_notifications: {
    disabled: false,
    disabled_until: null,
  },
  notification_settings: {
    mentions: { enabled: true },
    messages: { enabled: true, frequency: 'immediately' },
    follows: { enabled: true },
  },
});
```

---

### 15. Message Bookmarks & Reminders ⭐

**Why**: Help users save important content and come back to it.

**Implementation** (2025 feature - coming soon):

```javascript
// Bookmark a message
await channel.sendAction(messageId, {
  type: 'bookmark',
  user_id: userId,
});

// Get bookmarked messages
const bookmarks = await client.queryUsers({
  id: userId,
}).then(user => user.bookmarked_messages);

// Set a reminder
await channel.sendAction(messageId, {
  type: 'set_reminder',
  reminder_at: '2025-12-01T10:00:00Z',
});
```

---

### 16. Live Location Sharing ⭐

**Why**: Great for meetups, events, and location-based social features.

**Implementation** (2025 feature - coming soon):

```javascript
// Share current location
await channel.sendMessage({
  text: 'Meeting here!',
  location: {
    latitude: 37.7749,
    longitude: -122.4194,
    name: 'Cafe Momento',
  },
  attachments: [{
    type: 'location',
    latitude: 37.7749,
    longitude: -122.4194,
  }],
});

// Live location sharing
const locationShareId = await startLiveLocationShare({
  duration: 3600, // 1 hour in seconds
  interval: 30, // Update every 30 seconds
});
```

---

### 17. Read Receipts & Message Status ⭐⭐

**Why**: Transparency about message delivery and reading.

**Implementation** (automatic):

```javascript
// Already enabled by default
// Access read state:
const { read } = channel.state;

read.forEach(readState => {
  console.log(`${readState.user.name} last read: ${readState.last_read}`);
});

// Custom read receipt UI
import { useChannelStateContext } from 'stream-chat-react';

const ReadReceipts = ({ message }) => {
  const { read } = useChannelStateContext();

  const readBy = read.filter(r =>
    new Date(r.last_read) >= new Date(message.created_at)
  );

  return (
    <div className="read-receipts">
      {readBy.map(r => (
        <img key={r.user.id} src={r.user.image} alt={r.user.name} />
      ))}
    </div>
  );
};
```

---

### 18. URL Previews & Link Enrichment ⭐⭐

**Why**: Richer message experience; drives engagement with shared content.

**Implementation** (automatic):

```javascript
// Automatic URL enrichment is enabled by default
// When user sends: "Check out https://example.com"
// GetStream automatically fetches and adds:
// - Title
// - Description
// - Image
// - Favicon

// Access enriched data:
message.attachments.forEach(attachment => {
  if (attachment.type === 'url') {
    console.log(attachment.og_scrape_url);
    console.log(attachment.title);
    console.log(attachment.description);
    console.log(attachment.image_url);
  }
});
```

**Custom Link Preview Component**:

```javascript
const LinkPreview = ({ attachment }) => {
  if (attachment.type !== 'url') return null;

  return (
    <div className="link-preview">
      <img src={attachment.image_url} alt={attachment.title} />
      <div>
        <h4>{attachment.title}</h4>
        <p>{attachment.description}</p>
        <a href={attachment.og_scrape_url}>Visit</a>
      </div>
    </div>
  );
};
```

---

## Phase 5: Analytics & Optimization (Week 9-10)

### 19. Custom Events & Analytics ⭐⭐

**Why**: Understand user behavior and optimize the experience.

**Implementation**:

```javascript
// Track custom events
await client.trackEvent({
  type: 'profile_view',
  user_id: viewerId,
  target_user_id: profileUserId,
});

await client.trackEvent({
  type: 'post_share',
  user_id: sharerId,
  post_id: postId,
  platform: 'twitter',
});

// Activity Feed analytics
await userFeed.addActivity({
  actor: userId,
  verb: 'view',
  object: 'post:123',
  analytics: {
    source: 'feed',
    position: 3,
  },
});
```

**Engagement Metrics**:

```javascript
// Get channel analytics
const channelStats = await channel.query({
  messages: { limit: 0 },
  members: { limit: 0 },
  state: false,
});

console.log(channelStats.channel.member_count);
console.log(channelStats.channel.message_count);
console.log(channelStats.channel.created_at);
```

---

### 20. Webhooks for Custom Logic ⭐⭐

**Why**: Integrate with your backend systems, analytics, and business logic.

**Setup** (in GetStream Dashboard):

1. Go to App Settings > Webhooks
2. Add your webhook URL
3. Select events to listen to

**Webhook Handler Example**:

```javascript
// Express.js webhook endpoint
app.post('/webhooks/stream', async (req, res) => {
  const event = req.body;

  switch(event.type) {
    case 'message.new':
      // Store in your database
      await saveMessageToDb(event.message);
      // Update user stats
      await updateUserActivityStats(event.user.id);
      break;

    case 'user.banned':
      // Notify admins
      await notifyAdmins(`User ${event.user.id} was banned`);
      break;

    case 'reaction.new':
      // Award points for engagement
      await awardEngagementPoints(event.user.id, 5);
      break;
  }

  res.status(200).send('OK');
});
```

**Available Events**:
- `message.new`, `message.updated`, `message.deleted`
- `reaction.new`, `reaction.deleted`
- `member.added`, `member.removed`
- `channel.created`, `channel.updated`
- `user.banned`, `user.unbanned`
- And 50+ more events

---

## Implementation Roadmap

### Week 1-2: Chat Foundation
- ✅ Message Reactions
- ✅ Threaded Conversations
- ✅ Pinned Messages
- ✅ User Presence & Typing
- ✅ Message Search

**Impact**: Dramatically improves chat UX to match best-in-class apps like Slack/Discord.

---

### Week 3-4: Social Features
- ✅ Activity Feeds - "For You" personalized feed
- ✅ Stories (ephemeral content)
- ✅ Notifications feed
- ✅ Groups & Forums

**Impact**: Transforms Six from chat app to full social platform with content discovery.

---

### Week 5-6: Rich Media & AI
- ✅ Video & Audio Calls
- ✅ Live Streaming
- ✅ AI Chatbot Integration
- ✅ AI Content Moderation

**Impact**: Premium features that differentiate Six from competitors; essential for scale.

---

### Week 7-8: Engagement
- ✅ Push Notifications V4
- ✅ Message Bookmarks & Reminders
- ✅ Live Location Sharing
- ✅ Read Receipts
- ✅ URL Previews

**Impact**: Drives retention and daily active usage through re-engagement and utility.

---

### Week 9-10: Analytics & Scale
- ✅ Custom Events & Analytics
- ✅ Webhooks Integration
- ✅ Performance Optimization
- ✅ Scale Testing

**Impact**: Data-driven optimization and business intelligence.

---

## Quick Start Checklist

### Environment Setup

```bash
# Install all GetStream packages
npm install stream-chat stream-chat-react @stream-io/video-react-sdk getstream

# Import CSS
# In your main app file:
import 'stream-chat-react/dist/css/v2/index.css';
```

### Get API Keys

1. Sign up at https://getstream.io/
2. Create a new app
3. Get your API Key and Secret
4. Generate user tokens (server-side)

### Server-Side Token Generation

```javascript
// Node.js backend
const StreamChat = require('stream-chat').StreamChat;

const serverClient = StreamChat.getInstance(
  process.env.STREAM_API_KEY,
  process.env.STREAM_API_SECRET
);

// Generate token for user
const token = serverClient.createToken(userId);
```

### Initialize in React

```javascript
import { useCreateChatClient } from 'stream-chat-react';

function App() {
  const client = useCreateChatClient({
    apiKey: process.env.REACT_APP_STREAM_API_KEY,
    tokenOrProvider: userToken,
    userData: { id: userId, name: userName, image: userImage },
  });

  if (!client) return <div>Loading...</div>;

  return (
    <Chat client={client}>
      {/* Your app */}
    </Chat>
  );
}
```

---

## Performance Optimization Tips

### 1. Lazy Load Components

```javascript
import { lazy, Suspense } from 'react';

const VideoCallUI = lazy(() => import('./VideoCallUI'));
const LiveStream = lazy(() => import('./LiveStream'));

<Suspense fallback={<LoadingSpinner />}>
  <VideoCallUI />
</Suspense>
```

### 2. Pagination for Feeds

```javascript
// Always paginate feed results
const feed = await userFeed.get({
  limit: 25,
  offset: page * 25,
  enrich: true,
  reactions: { recent: true, counts: true, own: true }
});
```

### 3. Channel List Optimization

```javascript
<ChannelList
  options={{
    presence: true,
    state: true,
    watch: true,
    limit: 30, // Don't load all channels at once
  }}
  sort={{ last_message_at: -1 }}
  filters={{
    members: { $in: [userId] },
    type: 'messaging'
  }}
/>
```

### 4. Unsubscribe from Listeners

```javascript
useEffect(() => {
  const handleNewMessage = (event) => {
    // Handle message
  };

  client.on('message.new', handleNewMessage);

  return () => {
    client.off('message.new', handleNewMessage);
  };
}, [client]);
```

---

## Cost Optimization

### Leverage Caching
- GetStream's global edge network provides 5-9ms response times
- Results are cached automatically
- Use `maxAge` cache headers where appropriate

### Message Retention Policies
- Set appropriate retention periods for older messages
- Archive inactive channels
- Use truncate for large channels

### Optimize Media Storage
- Use GetStream's CDN for images/files
- Compress images before upload
- Set up automatic cleanup for ephemeral content (stories)

---

## Security Best Practices

### 1. Never Expose API Secret Client-Side

```javascript
// ❌ WRONG - Never do this
const client = new StreamChat(apiKey, apiSecret);

// ✅ CORRECT - Generate tokens server-side
const token = await fetch('/api/stream-token').then(r => r.json());
const client = new StreamChat(apiKey);
await client.connectUser({ id: userId }, token);
```

### 2. Use Permissions & Roles

```javascript
// Set up channel-level permissions
const channel = client.channel('messaging', 'general', {
  name: 'General Chat',
  members: [userId],
  // Only admins can pin messages
  pin_message: ['admin'],
  // Only moderators can delete any message
  delete_any_message: ['admin', 'moderator'],
});
```

### 3. Enable Content Moderation

```javascript
// In Dashboard: Enable AI Moderation
// Set up automod rules
// Configure webhooks for flagged content
```

---

## Testing Strategy

### Unit Tests

```javascript
import { renderHook } from '@testing-library/react-hooks';
import { useCreateChatClient } from 'stream-chat-react';

test('creates chat client with valid credentials', async () => {
  const { result, waitForNextUpdate } = renderHook(() =>
    useCreateChatClient({
      apiKey: 'test-key',
      tokenOrProvider: 'test-token',
      userData: { id: 'user-1' },
    })
  );

  await waitForNextUpdate();
  expect(result.current).toBeDefined();
});
```

### Integration Tests

```javascript
import { StreamChat } from 'stream-chat';

test('sends and receives messages', async () => {
  const client = StreamChat.getInstance(apiKey);
  await client.connectUser({ id: 'test-user' }, token);

  const channel = client.channel('messaging', 'test-channel');
  await channel.watch();

  const message = await channel.sendMessage({ text: 'Hello!' });
  expect(message.message.text).toBe('Hello!');

  await client.disconnectUser();
});
```

---

## Support & Resources

### Official Documentation
- **Chat SDK**: https://getstream.io/chat/docs/sdk/react/
- **Video SDK**: https://getstream.io/video/docs/react/
- **Activity Feeds**: https://getstream.io/activity-feeds/docs/
- **API Reference**: https://getstream.io/chat/docs/api/

### Community
- **GitHub**: https://github.com/GetStream
- **Support**: Every docs page has a "!?" icon to contact the team
- **Slack Community**: https://getstream.io/slack

### Additional Resources
- [Message Reactions](https://getstream.io/chat/docs/sdk/react/components/message-components/reactions/)
- [Threading Documentation](https://getstream.io/chat/docs/react/threads/)
- [Pinned Messages](https://getstream.io/chat/docs/react/pinned_messages/)
- [2025 Product Roadmap](https://getstream.io/blog/product-roadmap-2025/)

---

## Next Steps

1. **Set up GetStream account** and get API keys
2. **Implement Phase 1 features** (Message Reactions, Threading, Pinned Messages)
3. **Test with real users** to validate UX improvements
4. **Add Activity Feeds** for content discovery (Phase 2)
5. **Integrate AI Moderation** before scaling (Phase 3)
6. **Add Video/Audio** for premium features (Phase 3)
7. **Optimize & Scale** based on usage patterns (Phase 5)

---

**Questions?** Contact GetStream support or review the comprehensive documentation linked throughout this guide.

**Pro Tip**: Start with the features marked ⭐⭐⭐ for maximum impact. Many features work out-of-the-box with minimal code!
