var pubnub = new PubNub({
    publishKey: 'pub-c-c2c653ff-69ef-4ffc-afba-3c2cac4a05c2',
    subscribeKey: 'sub-c-98a5ebee-06bc-11e6-bbd9-02ee2ddab7fe'
});

eon.map({
    pubnub: pubnub,
    id: 'map',
    mbToken: 'pk.eyJ1Ijoia2JvaCIsImEiOiJjajFlbTlrNjIwMDV6MzNtdm45NHhkbTIwIn0.gGez9OLnJeKyVl3kHfWqCg',
    mbId: 'kboh',
    channels: ['eon-map']
});

setInterval(function () {
    pubnub.publish({
        channel: 'eon-map',
        message: [
            {"latlng": [31, -99]},
            {"latlng": [32, -100]},
            {"latlng": [33, -101]},
            {"latlng": [35, -102]}
        ]
    });
}, 1000);