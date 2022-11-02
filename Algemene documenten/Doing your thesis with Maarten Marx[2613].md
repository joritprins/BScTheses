# Doing your thesis with Maarten Marx

Hi, happy to supervise your thesis. I supervise quite a number of students and created a system to do this smoothly and with high chance of success. Here we go:

1. Register yourself at <https://forms.gle/yVRk4tosF4rkaYCp8>
2. Create a **private** github repo for your thesis and invite me (`maartenmarx`) and ,if you have , other supervisors.

## Github repo

THis contains **everything related to your thesis**, nicely organized in folders.


1. A folder for the Latex files of your thesis, including the pdf.
    2. If you work on Overleaf, you can link that account to your repo
    3. If you work on Overleaf, put the URL large in your README.md
3. A folder with notebooks containing experiments, etc
4. Maybe a literature folder
5. A personal folder with your CV and your gradelist and whatever more you want to share with me.  
6.  [Great github repo template at the Gemeente Amsterdam](https://github.com/Amsterdam-Internships/InternshipAmsterdamGeneral)


### Overleaf

* New in 2022: [Templates for the master IS](https://www.overleaf.com/read/bctyrsjktnrx) (for thesis design, reports and the final thesis). This is a read only link. Download the source and start a new project with it.


Many of you prefer overleaf for their thesis. I am fine with that, but please stick to these guidelines to keep you orgamized and me sane

1. Put the URL to your overleaf project LARGE in your github readme.
2. Organize your overleaf project well, as follows:
3. Create directories for 
    4. images
    5. preamble and style files
    6. sections
        7. For each section you create a seperate file which you include in `main.tex` at the top level.
        8. I suggest to use [the subfiles package](https://www.overleaf.com/learn/latex/Multi-file_LaTeX_projects), which is really nice and easy, and saves a lot of hassle.
    9. bib stuff
8. Top level contains `main.tex`  and the folders, and I guess that is it.


# How to make and keep everyone happy 
* Read, read, reread and use it daily in everything you do, but first of all in all you comunicate, [this advice by Eamonn Keogh ](https://www.cs.ucr.edu/~eamonn/public/SDM_How_to_do_Research_Keogh.pdf)

> If you can save the reviewer one minute of their time, by spending one extra hour of your time, then you have an obligation to do so. [page 75]



#### Thesis itself

1. Follow provided templates of your study. For more tips on layout etc, see [my template for MSc DS](https://github.com/maartenmarx/ThesisTemplate/tree/master/ThesisTemplate)
2. Use `\tableofcomntents`, `\hyperref` and number lines and pages
3. Make seperate files for each section and clean folders and use `\input`
4. If you use Overleaf, set the url to the main tex file large in your `readme.md` on github (then I can find it back).





## Weekly updates

Every week before Friday 09:00 you post a new issue entitled *update `the date of today`* , where ypou @-mention me and in which you describe 

* what you have achieved,
    *   with hyperlinks to the notebooks or pdf (indicate exactly where) in which this is reported
*   what did **not** work out
*   what you plan to achieve next week
*   if you want to ask me something/discuss something
    *   clearly stated questions/discussion points
    *   preferably with hyperlinks to material/notebooks

## Communication and meetings

* All communication via github issues in which you mention or assign me.
* Biweekly zoom meetings on either a fixed timeslot or we vary, depending how it goes. 
    * If needed we can always meet more or less often

## Group supervision

During Corona I started with group supervsion, which worked out very well. Groups of 3-4 persons, working on similar projects. Benefits:

* you can learn a lot from each other
* you see that others have the same problems/troubles/frustrations/... as you
* you are not alone
* you can do peer reviewing/helping
    *   eg, read each others introduction and criticize/help

Depending on my students I might do that as well. Then usually we all open up our github repos to each other.    

## Grades and passing

I like good quality. If you want to aim for a high grade ("good" or higher ($\geq 8$), and I think your work is worth it I will fight for you and your grade. Many of my students won awards with their thesis or could present it at a workshop or conference. Also many who did an internship at a company got an offer to stay there after their thesis.

Almost all of my thesis students pass in the time which is given for the thesis project (so for an 18EC thesis, this is 3 months full time). I like that and I will help you and push you meet this "deadline".

My mean and median grade is in line with the mean and median of the study: "satisfactory" (in Dutch *bevredigend*), which is a 7 or 7.5. 


### How to "satisfy" the independent examiner


Nog even een tip. Probeer toch die onafhankelijke examinator die ik niet ken, en met wie ik ook niet praat in gedachten te nemen en te kijken hoe je die kunt **behagen**. Hier geef ik een heel veel gebruikte volgorde van lezen van een artikel. **Gebruik dit als je weinig tijd hebt, om te zorgen dat die delen allemaal perfect zijn.** 

1. Die andere examinator heeft maar heel weinig tijd, en dit moet even tussendoor.
2. Die leest je scriptie als volgt:
   * abstract
   * zoekt de ondxerzoeksvragen op, als ze die niet in een paar tellen gevonden heeft wordt ze al kribbig
   * leest die heel nauwkeurig, en probeert zich het antwoord voor te stellen
      * is dat rottig , een gedoe of onmogelijk, dan zit je al op een 7-7.5 maximaal
   * gaat dan op zoek naar de antwoorden in de conclusie en in tabelletjes/grafiekjes in je resultaten
      * is dat te vinden en gebeurt er iets spannends, dan gaat ze verder lezen of hier allicht ook een 8 of hoger in zit
      * anders is het of een default 7 of 7.5, of als er gekke dingen in zitten, lager, en dan gaat ze verder kijken of dat nou aan haar ligt of dat er echt gekke dingen gebeuren/ommissies zijn.

      
## Publication

I strongly encourage this.
The Master IS as well: 

### support
The master IS program (financially) supports students whose thesis work gets accepted for conference or publication. Students can reimburse costs up to 1000 Euro’s via: <https://expenseclaims.uva.nl/?language=en>. They need to  upload copy of receipts and enter the following information: 
 
reference number (wbs): R.2318.0040.01
contact person:Dr. Sennay Ghebreab
phone number: 020-5252270
