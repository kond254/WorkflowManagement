
import { Component, OnInit } from '@angular/core';
import jobinformationData from '../../assets/jobinformation.json';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
import candidateData from '../../assets/candidates.json';
import jobinformationacceptedData from '../../assets/jobinformationaccepted.json';
import topcanidatesData from '../../assets/TopCandidates.json';
// /*
// *
// *
// */
import { DataServiceInterface } from '../data.service';

interface JobOffer {
  processID: number;
  professionTitel:string;
  professionType:string;
  numberProfessions: string;
  discription:string; 
}
// Importiert aus hrdepartmenmt
interface JobStandards{
  processID: number;
  jobTitel: string;
  jobType: string;
  reguiredExperience: number;
  jobDescription: string;
  responsibilities: string;
  location: string;
  jobMode: string;
  weeklyHours: number;
  annualSalary: number;
  paidtimeoff: number;
  benefits: string;
  industry: string;
  graduationLevel: string; 
  language: string;
  numberOfPositions: number;
}


@Component({
  selector: 'app-hrmanager',
  templateUrl: './hrmanager.component.html',
  styleUrl: './hrmanager.component.css'
})
export class HrmanagerComponent implements OnInit {
  acceptedJobsWithCandidates: { job: any; candidates: any[] }[] = [];
  selectedJob: { job: any; candidates: any[] } | null = null;

  // ... deine anderen Deklarationen hier ...

 // nach dem vorbild des HR Department angelegt wo auch jobOffer so angelegt wurde
  jobStandards: JobStandards = {
    processID: 0,
    jobTitel: '',
    jobType: '',
    reguiredExperience: 0,
    jobDescription: '',
    responsibilities: '',
    location: '',
    jobMode: '',
    weeklyHours: 0,
    annualSalary: 0,
    paidtimeoff: 0,
    benefits: '',
    industry: '',
    graduationLevel: '',
    language: '',
    numberOfPositions: 0
  };



  ngOnInit() {
    this.listAcceptedJobsWithCandidates();
  }

  listAcceptedJobsWithCandidates(): void {
    this.acceptedJobsWithCandidates = [];

    for (const job of this.dataJobInformationAccepted) {
      const candidatesForJob = this.newtopcanidates.filter(candidate => candidate.cID === job.id);
      this.acceptedJobsWithCandidates.push({ job, candidates: candidatesForJob });
    }
  }

  showCandidatesForJob(job: any): void {
    const candidatesForJob = this.newtopcanidates.filter(candidate => candidate.cID === job.id);
    this.selectedJob = { job, candidates: candidatesForJob };
  }
  
  
  
  
  professionTitel:string ='';
  professionType:string ='';
  graduactionLevel:string ='';
  location:string ='';
  salary: string ='';
  numberEmployees: string ='';
  info:string ='';

  jobtitle:string ='';
  number:string = '';
  additionalinformation:string ='';

  id: string ='';
 

  cname: string = '';
  ceducation: string = '';
  clocation: string = '';
  csalary: string = '';
  cinfo: string= '';
  cid: string = '';

 

  newjobOffer: {
    professionTitel: string;
    professionType: string;
    graduactionLevel: string;
    location: string;
    salary: string;
    numberEmployees: string;
    info: string
  }[] = [];

  newjobInformation: {
    jobtitle: string;
    number: string;
    location: string;
    salary: number;
    additionalinformation: string;
  }[] = jobinformationData;


  newtopcanidates: {
    cname : string;
    ceducation : string;
    clocation : string;
    csalary : number;
    cage : number;
    cinfo : string;
    cID : string;
  } [] = topcanidatesData;


  dataNews: any[] = [];
  data: JobOffer[]=[];
  // newjobOffer: JobOffer[] = [];

  newjobinformationaccepted: {
    jobtitle: string;
    number: string;
    location: string;
    salary: number;
    additionalinformation: string;
    id: string;
  }[] = jobinformationacceptedData;



  /*
      #insert job standards in the table
    def insert_job_standards_in_db(self, process_id: int, jobType: str, jobTitle:str, required_experience: int, job_description: str, responsibilities:str, location:str, job_mode:str, weekly_hours: int, pay: int, pto: int, benefits: str, industry:str, min_education_level:str, language:str, numberOfPositions: int):
        #finding file in the sql folder
        with open('SQL/insertIntoJobStandards.sql', 'r') as sql_file:
            sql_script = sql_file.read()           
            #generating json format
            data = {
            'job_process_instance_key': process_id,
            'jobTitle': jobTitle,
            'jobType': jobType,
            'required_experience': required_experience,
            'job_description': job_description,
            'responsibilities': responsibilities,
            'location': location,
            'job_mode': job_mode,
            'weekly_hours': weekly_hours,
            'AnnualSalary': pay,
            'pto': pto,
            'benefits': benefits,
            'industry': industry,
            'min_education_level': min_education_level,
            'language': language,
            'numberOfPosition': numberOfPositions
        }
            #create a tuple for json format that the sql file can read the data
            cur.execute(sql_script, tuple(data.values()))
            con.commit()
            print("DB INSERT EXECUTED")

  */



  step = 0;

  
  constructor(private dataService: DataMessageService, private snackbarService: SnackbarService, private dataServiceInterface: DataServiceInterface) {}

////////////////////////////////////////////////////////////

// Hier ist die Funktion getJobOffer die in Zeile 146 aufgerufen wird!
//   async ngOnInit(): Promise<any> {
//     await this.getJobOffer();
//   }

///////////////////////////////////////////////////////////////

//   //Hier ist die Funktion um die Job Offer zu bekommen
//   async getJobOffer() {
//     this.dataServiceInterface.getJobOffer().subscribe(
//       data => {
//         this.data = data as JobOffer[]; // Assign the data to this.data
//         console.log(this.data)
//       },
//       error => {
//         console.error("Error fetching job offer data:", error);
//       }
//     );
//   }

//     //Funktion prüft, ob Job Information leer
//   // hasData(): boolean {
//   //   return this.data.length == 0 || this.newjobOffer.length == 0;
//   // }
///////////////////////////////////

  // Funktion setzt die Nummer der Pannel, für die Funktion Zurück/Vor
  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }

  // Initialisieren Sie das candidates-Array mit den Daten aus der JSON-Datei
  dataCandidate: { name: string; education: string; location: string; salary: number; age: number; info: string }[] = candidateData;
  dataJobInformation: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string }[] = jobinformationData;
  dataJobInformationAccepted: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string; id: string }[] = jobinformationacceptedData;
  datatopcanidatesData: { cname: string; ceducation: string; clocation: string; csalary: number; cage: number; cinfo: string; cID: string }[] = topcanidatesData;





  //Funktion prüft, ob candiates leer
  hasData(): boolean {
    return this.dataCandidate.some(data =>
      data.name.trim() !== '' &&
      data.education.trim() !== '' &&
      data.location.trim() !== '' &&
      data.info.trim() !== '' &&
      data.salary  !== 0 &&
      data.age  !== 0 &&
      data.info.trim()
    );
  }

    //Funktion prüft, ob Job Information leer

  hasJobInformation(): boolean {
    return this.dataJobInformation.some(data =>
      data.jobtitle.trim() !== '' &&
      data.number.trim() !== '' &&
      data.location.trim() !== '' &&
      data.additionalinformation.trim() !== '' &&
      data.salary !== 0
    );
  }

  hasJobInformationAccepted(): boolean {
    return this.dataJobInformationAccepted.some(data =>
      data.jobtitle.trim() !== '' &&
      data.number.trim() !== '' &&
      data.location.trim() !== '' &&
      data.additionalinformation.trim() !== '' &&
      data.id.trim() !== '' &&
      data.salary !== 0
    );
  }
  
 



  isValidForm(): boolean {
    return !(!this.professionTitel || !this.professionType || !this.graduactionLevel || !this.location || !this.salary || !this.numberEmployees);
  }

  // hasData(): boolean {
  //   return this.data.length == 0 || this.newjobOffer.length == 0;
  // }

  //Funktion speichert die Benutzer eingaben
  saveData(): void {
    const newData = {
      professionTitel: this.professionTitel,
      professionType: this.professionType,
      graduactionLevel: this.graduactionLevel,
      location: this.location,
      salary: this.salary,
      numberEmployees: this.numberEmployees,
      info: this.info,
    };

  // hier neuen Daten in Array
  this.newjobOffer.push(newData);
  // this.dataService.saveData(newData);


  this.snackbarService.showSuccess('New job information saved');
  this.resetJobInfoInputFields();

  }

      // Funktion speichert die Benutzereingabe
  saveJobInformation(): void {
    const newJobInfo = {
      jobtitle: this.professionTitel,
      number: this.numberEmployees,
      location: this.location,
      salary: parseFloat(this.salary),
      additionalinformation: this.info,
    };

  this.newjobInformation.push(newJobInfo);
    
  this.snackbarService.showSuccess('New job offer sent');
  this.resetInputFields();

  }
          

  resetInputFields():void{
    this.professionTitel = '';
    this.professionType = '';
    this.graduactionLevel = '';
    this.location = '';
    this.salary = '';
    this.numberEmployees = '';
    this.info = '';
  }

  resetJobInfoInputFields(): void {
    this.professionTitel = '';
    this.numberEmployees = '';
    this.location = '';
    this.salary = '';
    this.info = '';
  }

  resetJobInfoAcceptedInputFields(): void {
    this.professionTitel = '';
    this.numberEmployees = '';
    this.location = '';
    this.salary = '';
    this.info = '';
    this.id = ''; 
  }

  resettopcandidatesInputFields(): void {
    this.cname = '';
    this.ceducation = '';
    this.clocation = '';
    this.csalary = '';
    this.cinfo = '';
    this.cid = ''; 
    
    
 
  }

  
 //Hier werden die neuen Job Offer ans DataServiceInterface gesendet
 sendData() {}
/*   this.dataServiceInterface.sendJobStandards(this.jobStandards).subscribe(
    response => {
      console.log('Data sent successfully', response);
      this.snackbarService.showSuccess('New job standard sented');
      // Hier kannst du weitere Aktionen nach dem Senden durchführen, z.B., eine Erfolgsmeldung anzeigen
    },
    error => {
      console.error('Error sending data', error);
      // Hier kannst du Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
    }
  );
} */


  // Funktion, um den Job zu akzeptieren
  acceptJob(item: any): void {
    // hier die Logik zum Akzeptieren des Jobs implmentieren
    console.log('Job accepted:', item);
  }

  // Funktion, um den Job abzulehnen
  rejectJob(item: any): void {
    // hier die Logik zum Ablehnen des Jobs des Jobs implmentieren
    console.log('Job rejected:', item);
  }

  acceptCandidate(item: any): void {
    // hier die Logik zum Akzeptieren des Jobs implmentieren
    console.log('Job accepted:', item);
  }

  // Funktion, um den Job abzulehnen
  rejectCandidate(item: any): void {
    // hier die Logik zum Ablehnen des Jobs des Jobs implmentieren
    console.log('Job rejected:', item);
  }

  

 
}






          




