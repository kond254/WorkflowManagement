import { Component, OnInit } from '@angular/core';
import candidateData from '../../assets/candidates.json';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
/*
*
*
*/
import { DataServiceInterface } from '../data.service';

interface JobStandards{
  processID: number;
  jobTitel: string;
  JobType: string;
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
}


@Component({
  selector: 'app-hrdepartment',
  templateUrl: './hrdepartment.component.html',
  styleUrl: './hrdepartment.component.css',
  
})

export class HrdepartmentComponent implements OnInit {

  jobOffer: JobOffer = {
    processID: 0,
    professionTitel: '',
    professionType: '',
    numberProfessions: 0,
    description: ''
  };

  dataJobStandards: JobStandards[]=[];
  dataJobOffer: JobOffer[]=[];
  datacandidate: Candidate[]=[];
  // newjobOffer: JobOffer[] = [];

  newjobOffer: {
    professionTitel: string;
    professionType: string;
    graduactionLevel: string;
    location: string;
    salary: string;
    numberEmployees: string;
    info: string
  }[] = [];

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


  //Hier werden die neuen eingestellten Employees abgefragt vom DataServiceInterface
  // async getnewEmployees(){
  //   this.dataServiceInterface.getTopCandidate().subscribe(
  //     data => {
  //       this.data = data as Candidate[]; 
  //       console.log(this.data)
  //     },
  //     error => {
  //       console.error("Error fetching candidate data:", error);
  //     }
  //   );
  // }


   //Hier werden die neuen Job Offer abgefragt vom DataServiceInterface
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

  //Hier werden die neuen Job Offer ans DataServiceInterface gesendet
  sendData() {
    this.dataServiceInterface.sendJobOffer(this.jobOffer).subscribe(
      response => {
        console.log('Data sent successfully', response);
        this.snackbarService.showSuccess('New job offer sented');
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

  // Initialisieren Sie das candidates-Array mit den Daten aus der JSON-Datei

  //Funktion prüft, ob candiates leer
  //hasData(): boolean {
  //  return this.data.some(data =>
  //    data.name.trim() !== '' &&
   //   data.education.trim() !== '' &&
    //  data.location.trim() !== '' &&
     // data.info.trim() !== '' &&
      //data.salary  !== 0 &&
      //data.age  !== 0 &&
      //data.info.trim()
    //);
  //}
  // hasData(): boolean {
  //   return this.data.length == 0 || this.newjobOffer.length == 0;
  // }

  //Funktion speichert die Benutzer eingaben
  // saveData(): void {
  //   const newData = {
  //     professionTitel: this.professionTitel,
  //     professionType: this.professionType,
  //     numberEmployees: this.numberProfessions,
  //     info: this.discription,
  //   };
  //   console.log(newData)
  
  // // hier neuen Daten in Array
  // this.newjobOffer.push(newData);
  // // this.dataService.saveData(newData);

  
  // this.resetInputFields();
    
  // }

  // resetInputFields():void{
  //   this.professionTitel = '';
  //   this.professionType = '';
  //   this.numberProfessions = 0;
  //   this.discription = '';
  // }

}
