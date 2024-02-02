
import { Component, OnInit } from '@angular/core';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
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

interface TopCandidate {
  CandidateID: number;
  adress: string;
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
  hrmanagerAccepted: boolean; 
}

interface JobStandardsWithTopCandidates {
  AnnualSalary: number;
  Benefits: string;
  CandidateID: number;
  GraduationLevel: string;
  Industry: string;
  JobDescription: string;
  JobMode: string;
  JobTitle: string;
  JobType: string;
  Language: string;
  Location: string;
  PaidTimeOff: number;
  ProcessID: number;
  RequiredExperience: number;
  Responsibilities: string;
  WeeklyHours: number;
  address: string;
  age: number;
  city: string;
  country: string;
  email: string;
  first_name: string;
  gender: string;
  last_name: string;
  linkedin: string;
  numberOfPositions: number | null;
  previous_company: string;
  rating: number;
  zip_code: string;
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
dataJobOfferAccapted: JobOffer[]=[];
datacandidate: Candidate[]=[];   // ???????????????????????????
dataTopCandidate: TopCandidate[]=[];
dataJobStandardsWithTopCandidates: JobStandardsWithTopCandidates []=[];

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
    await this.getJobOfferAccapted();
    await this.getTopCandidate();
    
  }


  async getCandidate() {  //warum ist das hier??????????????????????????????brauchen das doch eigentlich nicht
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

  async getJobOfferAccapted() {
    this.dataServiceInterface.getJobOfferAccepted().subscribe(
      data => {
        this.dataJobOfferAccapted = data as JobOffer[];
        console.log(this.datacandidate)
      },
      error => {
        console.error("Error fetching candidate data:", error);
      }
    );
  }

  //Hier werden die neuen Job Standards abgefragt vom DataServiceInterface   
  async getjobStandards(){
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

   //Funktion ruft alle neuen top candidates vom DataServiceInterface ab
   async getTopCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.dataTopCandidate = data as TopCandidate[]; // Assign the data to this.data
        console.log(this.dataTopCandidate)
      },
      error => {
        console.error("Error fetching top candidate data:", error);
      }
    );
  } 

  async getJobStandardsWithTopCandidates(jobStandards: JobStandards) { 
    this.dataServiceInterface.getJobStandardsWithCandidates(jobStandards).subscribe(
      data => {
        this.dataJobStandardsWithTopCandidates = data as JobStandardsWithTopCandidates [];
        console.log(this.dataJobStandardsWithTopCandidates)
      },
      error => {
        console.error("Error fetching JobStandardsWithTopCandidates data:", error);
      }
    );
  }
  

  sendData(item: JobStandards) {
    this.dataServiceInterface.sendJobStandards(item).subscribe(
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
      this.getJobOffer();
      this.getJobOfferAccapted();
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
      this.getJobOffer();
      this.getJobOfferAccapted();
    },
    error => {
      console.error('Error delete job offer', error);
      // Hier können Sie Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
    }
  );
}
//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

acceptTopCandidate(item: TopCandidate): void {
  // Annahme-Logik hier implementieren
  console.log('Top candidate accepted:', item);

  // Die Variable hrmanagerAccepted auf true setzen

 item.hrmanagerAccepted = true; 

  // Die aktualisierten Daten an die Datenbank senden
  this.updateTopCandidate(item);
}

rejectTopCandidate(item: TopCandidate): void {
  // Ablehnungs-Logik hier implementieren
  console.log('Top candidate rejected:', item);

  // Das Job-Angebot aus der Datenbank löschen
  this.deleteTopCandidate(item);
}


// Methode zum Aktualisieren eines Job-Angebots in der Datenbank
updateTopCandidate(item: TopCandidate): void {
this.dataServiceInterface.updateTopCandidate(item).subscribe(
  response => {
    console.log('Top candidate updated successfully', response);
    this.snackbarService.showSuccess('Top candidate accepted');
    // Hier können Sie weitere Aktionen nach der Aktualisierung durchführen
    this.getTopCandidate();
    //this.getTopCandidateAccapted();
  },
  error => {
    console.error('Error updating top candidate', error);
    // Hier können Sie Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
  }
);

}

// Methode zum Löschen eines Job-Angebots aus der Datenbank
deleteTopCandidate(item: TopCandidate): void {
this.dataServiceInterface.deleteTopCandidate(item).subscribe(
  response => {
    console.log('Top candidate delete successfully', response);
    this.snackbarService.showSuccess('Top candidate rejected');
    // Hier können Sie weitere Aktionen nach der Aktualisierung durchführen
    this.getTopCandidate();
    //this.getTopCandidateAccapted();
  },
  error => {
    console.error('Error delete job offer', error);
    // Hier können Sie Aktionen im Fehlerfall durchführen, z.B., eine Fehlermeldung anzeigen
  }
);
}

/////////////////////////////////////////////////////////////




}
