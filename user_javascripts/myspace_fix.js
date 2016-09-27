//
// Opera takes too long to handle all the video/audio players so take them out
//
if( location.hostname.indexOf('myspace.com') != -1 ) {
    window.opera.addEventListener(
        'BeforeEvent.load',
        function () {
            var embeds = document.embeds ; 
            for( var i = 0; i < embeds.length; i++ ) {
                embeds[i].parentNode.removeChild( embeds[i] ) ; 
            }
        },
        false
    )
}


