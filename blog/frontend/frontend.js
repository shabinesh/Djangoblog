if (Meteor.isClient) {
  Template.hello.helpers({
	articles: function (){
		var q = Session.get('q');
		Meteor.call('getArticles', q, function(err, results){
			if (!err){
				Session.set('articles', results);
			}else{
				console.log("error:", err);
			}
		});
		return Session.get('articles');
	}
  });

  Template.hello.events({
    'submit .search-form': function (event) {
		var q = event.target.q.value;
		Session.set('q', q);
		Meteor.call('getArticles', q, function(err, res){
			Session.set('articles', res);
    		});
		event.target.q.value = q;
		return false;
		}	
  });
}

if (Meteor.isServer) {
  Meteor.startup(function () {
    // code to run on server at startup	
  });
}

Meteor.methods({
	getArticles: function(q){
		if (Meteor.isServer){
			var url = 'http://localhost:8000/articles/json/'
			if (q !== undefined && q !== null){
				url += "?q=" + q;
			}
			res = HTTP.get(url);
			if (res.statusCode == 200){
				return res.content 
			 }else{
				throw new Meteor.Error(res.status_code, "Remote server responded status other than 200.");
			}
		}
	}
});
