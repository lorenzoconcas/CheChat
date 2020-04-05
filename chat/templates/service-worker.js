//questo file è il service worker richiesto dalle pwa, serve a mettere in cache certi file e pagine


var CACHE_NAME = 'chechat-cache-v2';
var urlsToCache = [
    '/',
    '/static/chat/css/chat.css',
    '/static/chat/css/dark.css',
    '/static/chat/css/light.css',
    '/static/chat/css/mobile.css',
    '/static/chat/css/login.css',
    '/static/chat/css/login_mobile.css',
    '/static/chat/css/fonts.css',
    '/static/chat/js/chat.js',
    '/static/chat/js/push.js',
    '/static/chat/js/gui.js',
    '/static/chat/js/reactor.js',
    '/static/favicon.ico',
    '/static/chat/icons/chat_icon.png',
    '/static/chat/icons/add_partecipant.png',
    '/static/chat/icons/contacts.png',
    '/static/chat/icons/dark_mode.png',
    '/static/chat/icons/delete_chat.png',
    '/static/chat/icons/new_chat.png',
    '/static/chat/icons/remove_contact.png',
    '/static/chat/icons/user_group.png',
    '/static/chat/icons/user_icon_1.png',
    '/static/chat/icons/user_icon_2.png',
    '/static/chat/icons/user_icon_3.png',
    '/static/chat/icons/user_icon_4.png',
    '/static/chat/icons/user_icon_5.png',
    '/static/chat/audio/notify.ogg',
];

self.addEventListener('install', function(event) {
  // Perform install steps
 event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
       cache.addAll(urlsToCache)
               .then(() => console.log('Assets added to cache'))
                .catch(err => console.log('Error while fetching assets : ', err));
       return cache;
      })
  );
});
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Cache hit - return response
        if (response) {
          return response;
        }
        return fetch(event.request);
      }
    )
  );
});
