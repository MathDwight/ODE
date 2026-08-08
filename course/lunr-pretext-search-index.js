var ptx_lunr_search_style = "textbook";
var ptx_lunr_docs = [
{
  "id": "syllabus",
  "level": "1",
  "url": "syllabus.html",
  "type": "Section",
  "number": "",
  "title": "Syllabus",
  "body": " Syllabus        Course Information  This is the syllabus for course name (MATH xxx, section xxx) for [term] 20xx. It is a [n] credit course.    Instructor  Prof. Lastname, Office Location, prof.lastname@example.edu .    Student Hours  TBD    Class meets  course times and location.    Course Description  course description from catalog    Prerequisite  list of prerequisites    Textbook and course materials   textbook name by textbook author.       Course Overview        Assessments and Grades     "
},
{
  "id": "sec-course-info-2",
  "level": "2",
  "url": "syllabus.html#sec-course-info-2",
  "type": "Paragraph (with a defined term)",
  "number": "",
  "title": "",
  "body": "course name (MATH xxx, section xxx) "
},
{
  "id": "Mod-0-breakdown",
  "level": "1",
  "url": "Mod-0-breakdown.html",
  "type": "Section",
  "number": "",
  "title": "Mod 0: Logistics and Foundations",
  "body": " Mod 0: Logistics and Foundations   Mod 0 is called Logistics and Foundations.  Before we start to study, we will discuss how to study and how to progress in this particular instance of MATH 340 Intro to Differential Equations. Expect to grow! Expect to work! Expect to learn! Expect to get stuck, but expect to get unstuck, too! Then repeat.  The assignments of the course are a proxy to help me assess your knowledge and learning, according to the contract we enter together as students and faculty at a institute of higher education within the tradition of the United States. We need to be familiar with the criteria to achieve final letter grades. The route features expertly-crafted markers aligned along a journey in the study of mathematics. Before taking a step, however, we will prepare for the trip: We consider where we are now; where are we headed; and, what we need to get there.  Keywords: , course schedule, group meetings, Mods, core projects.    "
},
{
  "id": "week-01",
  "level": "1",
  "url": "week-01.html",
  "type": "Section",
  "number": "",
  "title": "Week 1",
  "body": " Week 1   This is an outline of the topics we covered in the first week of class.     Wednesday, 26 August 2026      Thursday, 27 August 2026      Friday, 28 August 2026      Saturday, 29 August 2026      Sunday, 30 August 2026      Monday, 31 August 2026      Tuesday, 01 September 2026     "
},
{
  "id": "week-02",
  "level": "1",
  "url": "week-02.html",
  "type": "Section",
  "number": "",
  "title": "Week 2",
  "body": " Week 2   This is an outline of the topics we covered in the second week of class.     Wednesday, 02 September 2026      Thursday, 03 September 2026      Friday, 04 September 2026      Saturday, 05 September 2026      Sunday, 06 September 2026      Monday, 07 September 2026      Tuesday, 08 September 2026     "
},
{
  "id": "Mod-1-breakdown",
  "level": "1",
  "url": "Mod-1-breakdown.html",
  "type": "Section",
  "number": "",
  "title": "Mod 1: Recognizing ODEs and Their Solutions",
  "body": " Mod 1: Recognizing ODEs and Their Solutions   Mod 1 is called Recognizing ODEs and Their Solutions.  After internalizing the course set-up and considering plans of progress, we step into the world of differential equations. We need to recognize the landscape and that process starts with determining what is and isn't a differential equation. Identifying what kind of problem we face is central to developing our problem solving skills. Then, believe it or not, we will analyze solutions before we discuss techniques to arrive at solutions. We take time to construct quality checks and assurance factors for the work we submit. The mantra is as follows:   A solution we do not understand is no solution at all!     "
},
{
  "id": "week-03",
  "level": "1",
  "url": "week-03.html",
  "type": "Section",
  "number": "",
  "title": "Week 3",
  "body": " Week 3   This is an outline of the topics we covered in the third week of class.     Wednesday, 09 September 2026      Thursday, 10 September 2026      Friday, 11 September 2026      Saturday, 12 September 2026      Sunday, 13 September 2026      Monday, 14 September 2026      Tuesday, 15 September 2026     "
},
{
  "id": "week-04",
  "level": "1",
  "url": "week-04.html",
  "type": "Section",
  "number": "",
  "title": "Week 4",
  "body": " Week 4   This is an outline of the topics we covered in the third week of class.     Wednesday, 16 September 2026      Thursday, 17 September 2026      Friday, 18 September 2026      Saturday, 19 September 2026      Sunday, 20 September 2026      Monday, 21 September 2026      Tuesday, 22 September 2026     "
}
]

var ptx_lunr_idx = lunr(function () {
  this.ref('id')
  this.field('title')
  this.field('body')
  this.metadataWhitelist = ['position']

  ptx_lunr_docs.forEach(function (doc) {
    this.add(doc)
  }, this)
})
