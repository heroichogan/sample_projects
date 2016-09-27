//
// Remove the sidebar that breaks up story text.  Page is then easier to
// "read" with Opera voice.
//
if( location.hostname.indexOf('wired.com') != -1 ) {   
    window.opera.addEventListener(
        'BeforeEvent.load',
        function () {
            var x = document.getElementById( 'storyInsert' ) ;
            x.parentNode.removeChild(x) ; 
        },
        false
    )
}


