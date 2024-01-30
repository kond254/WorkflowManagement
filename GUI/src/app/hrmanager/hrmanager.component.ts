
import { Component, OnInit } from '@angular/core';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';

// import candidateData from '../../assets/candidates.json';
// import jobinformationacceptedData from '../../assets/jobinformationaccepted.json';
// import topcanidatesData from '../../assets/TopCandidates.json';
// import jobinformationData from '../../assets/jobinformation.json';
// /*
// *
// *
// */
import { DataServiceInterface } from '../data.service';

interface JobStandards{
  ProcessID: number;
  JobTitle: string;
  JobType: string;
  RequiredExperience: number;
  JobDescription: string;
  Responsibilities: string;
  Location: string;
  JobMode: string;
  WeeklyHours: number;
  AnnualSalary: number;
  PaidTimeOff: number;
  Benefits: string;
  Industry: string;
  GraduationLevel: string; 
  Language: string;
  numberOfPositions: number;
}

interface Candidate {
  CandidateID: number;
  ProcessID: number;
  address: string;
  age: number;
  city: string;
  country: string;
  email: string;
  first_name: string;
  gender: string;
  last_name: string;
  linkedin: string;
  previous_company: string;
  rating: number;
  zip_code: string;
}

interface JobOffer {
  description: string;
  numberProfessions: number;
  processID: number;
  professionTitel: string;
  professionType: string;
  hrmanagerAccepted: boolean;
  
}


@Component({
  selector: 'app-hrmanager',
  templateUrl: './hrmanager.component.html',
  styleUrl: './hrmanager.component.css'

})

export class HrmanagerComponent implements OnInit {
  // acceptedJobsWithCandidates: { job: any; candidates: any[] }[] = [];
  // selectedJob: { job: any; candidates: any[] } | null = null;

  // ... deine anderen Deklarationen hier ...

 // nach dem vorbild des HR Department angelegt wo auch jobOffer so angelegt wurde

 jobStandards: JobStandards = {
  ProcessID: 0,
  JobTitle: '',
  JobType: '',
  RequiredExperience: 0,
  JobDescription: '',
  Responsibilities: '',
  Location: '',
  JobMode: '',
  WeeklyHours: 0,
  AnnualSalary: 0,
  PaidTimeOff: 0,
  Benefits: '',
  Industry: '',
  GraduationLevel: '', 
  Language: '',
  numberOfPositions: 0
}

dataJobStandards: JobStandards[]=[];
dataJobOffer: JobOffer[]=[];
datacandidate: Candidate[]=[];

newjobStandards: {
  //ProcessID: number;
  JobTitle: string;
  JobType: string;
  RequiredExperience: number;
  JobDescription: string;
  Responsibilities: string;
  Location: string;
  JobMode: string;
  WeeklyHours: number;
  AnnualSalary: number;
  PaidTimeOff: number;
  Benefits: string;
  Industry: string;
  GraduationLevel: string; 
  Language: string;
  numberOfPositions: number
}[] = [];

// newjobOffer: JobOffer[] = [];



step = 0;


constructor(private dataService: DataMessageService, private snackbarService: SnackbarService,private dataServiceInterface: DataServiceInterface) {}

  async ngOnInit(): Promise<any> {
    await this.getCandidate();
    // await this.getnewEmployees();
    await this.getJobOffer();
    await this.getjobStandards();
  }


  async getCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.datacandidate = data as Candidate[];
        console.log(this.datacandidate)
      },
      error => {
        console.error("Error fetching candidate data:", error);
      }
    );
  }

  //Hier werden die neuen Job Standards abgefragt vom DataServiceInterface
  getjobStandards(){
    this.dataServiceInterface.getJobStandards().subscribe(
      data => {
        this.dataJobStandards = data as JobStandards[];
        console.log(this.dataJobStandards)
      },
      error => {
        console.error("Error fetching job standards data:", error);
      }
    );
  }

  async getJobOffer() {
    this.dataServiceInterface.getJobOffer().subscribe(
      data => {
        this.dataJobOffer = data as JobOffer[]; // Assign the data to this.data
        console.log(this.dataJobOffer)
      },
      error => {
        console.error("Error fetching job offer data:", error);
      }
    );
  }

  sendData() {
    this.dataServiceInterface.sendJobStandards(this.jobStandards).subscribe(
      response => {
        console.log('Data sent successfully', response);
        this.snackbarService.showSuccess('New job standards sented');
        // Hier kannst du weitere Aktionen nach dem Senden durchführen, z.B., eine Erfolgsmeldung anzeigen
      },
      error => {
        console.error('Error sending data', error);
        // Hier kannst du Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
      }
    );
  }

  // ngOnInit() {
  //   this.listAcceptedJobsWithCandidates();
  // }

  // listAcceptedJobsWithCandidates(): void {
  //   this.acceptedJobsWithCandidates = [];

  //   for (const job of this.dataJobInformationAccepted) {
  //     const candidatesForJob = this.newtopcanidates.filter(candidate => candidate.cID === job.id);
  //     this.acceptedJobsWithCandidates.push({ job, candidates: candidatesForJob });
  //   }
  // }

  // showCandidatesForJob(job: any): void {
  //   const candidatesForJob = this.newtopcanidates.filter(candidate => candidate.cID === job.id);
  //   this.selectedJob = { job, candidates: candidatesForJob };
  // }
  
  
  
  
  // professionTitel:string ='';
  // professionType:string ='';
  // graduactionLevel:string ='';
  // location:string ='';
  // salary: string ='';
  // numberEmployees: string ='';
  // info:string ='';

  // jobtitle:string ='';
  // number:string = '';
  // additionalinformation:string ='';

  // id: string ='';
 

  // cname: string = '';
  // ceducation: string = '';
  // clocation: string = '';
  // csalary: string = '';
  // cinfo: string= '';
  // cid: string = '';

 

  // newjobOffer: {
  //   professionTitel: string;
  //   professionType: string;
  //   graduactionLevel: string;
  //   location: string;
  //   salary: string;
  //   numberEmployees: string;
  //   info: string
  // }[] = [];

  // newjobInformation: {
  //   jobtitle: string;
  //   number: string;
  //   location: string;
  //   salary: number;
  //   additionalinformation: string;
  // }[] = jobinformationData;


  // newtopcanidates: {
  //   cname : string;
  //   ceducation : string;
  //   clocation : string;
  //   csalary : number;
  //   cage : number;
  //   cinfo : string;
  //   cID : string;
  // } [] = topcanidatesData;


  // dataNews: any[] = [];
  // data: JobOffer[]=[];
  // // newjobOffer: JobOffer[] = [];

  // newjobinformationaccepted: {
  //   jobtitle: string;
  //   number: string;
  //   location: string;
  //   salary: number;
  //   additionalinformation: string;
  //   id: string;
  // }[] = jobinformationacceptedData;



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


  /////////////////////////////////////////////////////////////////////////////////////////////////////////////



  acceptJob(item: JobOffer): void {
    // Annahme-Logik hier implementieren
    console.log('Job accepted:', item);
  
    // Die Variable hrmanagerAccepted auf true setzen
    item.hrmanagerAccepted = true;
  
    // Die aktualisierten Daten an die Datenbank senden
    this.updateJobOffer(item);
  }

  rejectJob(item: JobOffer): void {
    // Ablehnungs-Logik hier implementieren
    console.log('Job rejected:', item);
  
    // Das Job-Angebot aus der Datenbank löschen
    this.deleteJobOffer(item);
  }


  // Methode zum Aktualisieren eines Job-Angebots in der Datenbank
updateJobOffer(item: JobOffer): void {
  this.dataServiceInterface.updateJobOffer(item).subscribe(
    response => {
      console.log('Job offer updated successfully', response);
      this.snackbarService.showSuccess('Job offer accepted');
      // Hier können Sie weitere Aktionen nach der Aktualisierung durchführen
    },
    error => {
      console.error('Error updating job offer', error);
      // Hier können Sie Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
    }
  );
}

// Methode zum Löschen eines Job-Angebots aus der Datenbank
deleteJobOffer(item: JobOffer): void {
  this.dataServiceInterface.deleteJobOffer(item).subscribe(
    response => {
      console.log('Job offer delete successfully', response);
      this.snackbarService.showSuccess('Job offer rejected');
      // Hier können Sie weitere Aktionen nach der Aktualisierung durchführen
    },
    error => {
      console.error('Error delete job offer', error);
      // Hier können Sie Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
    }
  );
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////




  // Initialisieren Sie das candidates-Array mit den Daten aus der JSON-Datei
  // dataCandidate: { name: string; education: string; location: string; salary: number; age: number; info: string }[] = candidateData;
  // dataJobInformation: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string }[] = jobinformationData;
  // dataJobInformationAccepted: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string; id: string }[] = jobinformationacceptedData;
  // datatopcanidatesData: { cname: string; ceducation: string; clocation: string; csalary: number; cage: number; cinfo: string; cID: string }[] = topcanidatesData;





  //Funktion prüft, ob candiates leer
  // hasData(): boolean {
  //   return this.dataCandidate.some(data =>
  //     data.name.trim() !== '' &&
  //     data.education.trim() !== '' &&
  //     data.location.trim() !== '' &&
  //     data.info.trim() !== '' &&
  //     data.salary  !== 0 &&
  //     data.age  !== 0 &&
  //     data.info.trim()
  //   );
  // }

  //   //Funktion prüft, ob Job Information leer

  // hasJobInformation(): boolean {
  //   return this.dataJobInformation.some(data =>
  //     data.jobtitle.trim() !== '' &&
  //     data.number.trim() !== '' &&
  //     data.location.trim() !== '' &&
  //     data.additionalinformation.trim() !== '' &&
  //     data.salary !== 0
  //   );
  // }

  // hasJobInformationAccepted(): boolean {
  //   return this.dataJobInformationAccepted.some(data =>
  //     data.jobtitle.trim() !== '' &&
  //     data.number.trim() !== '' &&
  //     data.location.trim() !== '' &&
  //     data.additionalinformation.trim() !== '' &&
  //     data.id.trim() !== '' &&
  //     data.salary !== 0
  //   );
  // }
  
 



  // isValidForm(): boolean {
  //   return !(!this.professionTitel || !this.professionType || !this.graduactionLevel || !this.location || !this.salary || !this.numberEmployees);
  // }

  // hasData(): boolean {
  //   return this.data.length == 0 || this.newjobOffer.length == 0;
  // }

  //Funktion speichert die Benutzer eingaben
  // saveData(): void {
  //   const newData = {
  //     professionTitel: this.professionTitel,
  //     professionType: this.professionType,
  //     graduactionLevel: this.graduactionLevel,
  //     location: this.location,
  //     salary: this.salary,
  //     numberEmployees: this.numberEmployees,
  //     info: this.info,
  //   };

  // hier neuen Daten in Array
  // this.newjobOffer.push(newData);
  // // this.dataService.saveData(newData);


  // this.snackbarService.showSuccess('New job information saved');
  // this.resetJobInfoInputFields();

  // }

      // Funktion speichert die Benutzereingabe
  // saveJobInformation(): void {
  //   const newJobInfo = {
  //     jobtitle: this.professionTitel,
  //     number: this.numberEmployees,
  //     location: this.location,
  //     salary: parseFloat(this.salary),
  //     additionalinformation: this.info,
  //   };

  // this.newjobInformation.push(newJobInfo);
    
  // this.snackbarService.showSuccess('New job offer sent');
//   this.resetInputFields();

//   }
          


  
//  //Hier werden die neuen Job Offer ans DataServiceInterface gesendet
//  sendData() {}
// /*   this.dataServiceInterface.sendJobStandards(this.jobStandards).subscribe(
//     response => {
//       console.log('Data sent successfully', response);
//       this.snackbarService.showSuccess('New job standard sented');
//       // Hier kannst du weitere Aktionen nach dem Senden durchführen, z.B., eine Erfolgsmeldung anzeigen
//     },
//     error => {
//       console.error('Error sending data', error);
//       // Hier kannst du Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
//     }
//   );
// } */




//   acceptCandidate(item: any): void {
//     // hier die Logik zum Akzeptieren des Jobs implmentieren
//     console.log('Job accepted:', item);
//   }

//   // Funktion, um den Job abzulehnen
//   rejectCandidate(item: any): void {
//     // hier die Logik zum Ablehnen des Jobs des Jobs implmentieren
//     console.log('Job rejected:', item);
//   }


 
}








          




