var mapTags = function() {
    var tags = this.tags;
    if (tags) {
        for (var i = tags.length - 1; i >= 0; i--) {
            if (tags[i])  {      // make sure there's something
               emit(tags[i].toLowerCase(), 1); // store a 1 for each word
            }
        }
    }
};


var reduceTags = function( key, values ) {
    var count = 0;
    values.forEach(function(v) {
        count +=v;
    });
    return count;
};



db.dotmarks.mapReduce(mapTags, reduceTags, {out: "tags"})
