db.question_all.remove({"question_url":/http:\/\/club.xywy.com\/106/})

db.question_all.find().forEach(
    function(item) {
        db.question_all.update({"_id":item._id}, {$set:{"post_date":item.question_url.split("/")[4],"post_month":item.question_url.split("/")[4].substring(0,6)}})
    })


db.question_all.find().forEach(
    function(item) {
        if (item.question_url:/static/) {
            db.question_all.update({"_id":item._id}, {$set:{"post_date":item.question_url.split("/")[4],"post_month":item.question_url.split("/")[4].substring(0,6)}})
        }
        elif (item.question_url:/question/){
            db.question_all.update({"_id":item._id}, {$set:{"post_date":item.question_url.split("/")[4],"post_month":item.question_url.split("/")[4].substring(0,6)}})

        }
        else{
        //
        }
    })

db.question_all.find().forEach(
    function(item) {
        db.question_all.update({"_id":item._id}, {$set:{"post_month":item.post_date.substring(0,6)}})
    })





db.question.find().forEach(
    function(item) {
        db.question.update({"_id":item._id}, {$set:{"post_date":item.question_url.split("/")[4]}})
    })


db.question.find().forEach(
    function(item) {
        db.question.update({"_id":item._id}, {$set:{"post_date":item.question_url.split("/")[4],"post_month":item.question_url.split("/")[4].substring(0,6)}})
    })

db.question.aggregate(
   [
     {
       $project:
          {
            item: 1,
            post_month: { $substr: [ "$post_date", 0, 6 ] },
          }
      }
   ]
)


#分组统计个数
db.question_all.aggregate({$match:{disease:"肿瘤科"}},{$group:{_id:"$post_month", disease:"$disease",number:{$sum:1}}})
db.question_all.aggregate({$match:{disease:"肿瘤科"}},{$group:{_id:"$post_month",number:{$sum:1}}},{$sort:{_id:1}})

db.department.find({disease_url:{$nin:db.question_all.distinct("disease_url",{department:{$exists:true}})}}).forEach(
    function(item) {
        db.question_all.update({"disease_url":item.disease_url},{$set:{"department":item.first_name,"department_url":item.first_url}},{multi:true})
    })

db.question_all.find({$and:[{department:{$exists:false}},{"disease_url":/http:\/\/club.xywy.com/}]}).forEach(
    function(item) {
        var department = db.department.find({"disease_url":item.disease_url},{"first_name":1,"first_url":1}).next()
        var department_name = department["first_name"]
        var department_url = department['first_url']
        db.question_all.update({"_id":item._id},{$set:{"department":department_name,"department_url":department_url}})
        }
    )

db.question_all.find({department:{$exists:false}},{$nor:[{"disease_url":""}]}).count()

db.question_all.find({$and:[{department:{$exists:false}},{"disease_url":/http:\/\/club.xywy.com/}]}).count()
db.question_all.find({$and:[{department:{$exists:false}},{"disease_url":""}]}).count()
db.question_all.find({department:{$exists:true}}).count()
db.question_all.find({"disease_url":""}).count()

db.department.find({disease_url:{$nin:db.question_all.distinct("disease_url",{department:{$exists:true}})}}).pretty()