import { Component, OnInit } from '@angular/core';
// import candidateData from '../../assets/candidates.json';
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
}

interface JobOffer {
  description: string;
  numberProfessions: number;
  processID: number;
  professionTitel: string;
  professionType: string;
}

interface NewEmployees{
  CandidateID: number;
  JopType: string;
  JobTitle: string;
  first_name: string;
  last_name: string;
  gender: string;
  email: string;
  linkedin: string;
  adress: string;
  city: string;
  zip_code: string;
  country: string;
  age: number;
  previous_company: string;
  rating: number;
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
  dataTopCandidate: TopCandidate[]=[];
  dataNewEmployess: NewEmployees[]=[];

  step = 0;

  constructor(private dataService: DataMessageService, private snackbarService: SnackbarService,private dataServiceInterface: DataServiceInterface) {}

  async ngOnInit(): Promise<any> {
    await this.getTopCandidate();
    await this.getnewEmployees();
    await this.getJobOffer();
    await this.getjobStandards();
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

  //Hier werden die neuen top candidates abgefragt vom DataServiceInterface
  getTopCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.dataTopCandidate = data as TopCandidate[];
        console.log(this.dataTopCandidate);
        console.error("Data top candidates retrieved");
      },
      error => {
        console.error("Error fetching candidate data:", error);
      }
    );
  }

  //Hier werden die neuen Job Offer abgefragt vom DataServiceInterface
  getJobOffer() {
    this.dataServiceInterface.getJobOffer().subscribe(
      data => {
        this.dataJobOffer = data as JobOffer[];
        console.log(this.dataJobOffer);
        console.error("Data job offer retrieved");
      },
      error => {
        console.error("Error fetching job offer data:", error);
      }
    );
  }


  //Hier werden die neuen Job Standards abgefragt vom DataServiceInterface
  getjobStandards(){
    this.dataServiceInterface.getJobStandards().subscribe(
      data => {
        this.dataJobStandards = data as JobStandards[];
        console.log(this.dataJobStandards)
        console.error("Data job standards retrieved");
      },
      error => {
        console.error("Error fetching job standards data:", error);
      }
    );
  }


    //Hier werden die neuen eingestellten Employees abgefragt vom DataServiceInterface
    async getnewEmployees(){
      this.dataServiceInterface.getNewEmployees().subscribe(
        data => {
          this.dataNewEmployess = data as NewEmployees[]; 
          console.log(this.dataNewEmployess)
          console.error("Data new employees retrieved");
        },
        error => {
          console.error("Error fetching new employee data:", error);
        }
      );
    }
  
  
  //Hier werden die neuen Job Offer ans DataServiceInterface gesendet
  sendData() {
    this.dataServiceInterface.sendJobOffer(this.jobOffer).subscribe(
      response => {
        console.log('Data job offer sent successfully', response);
        this.snackbarService.showSuccess('New job offer sented');
      },
      error => {
        console.error('Error sending job offer data', error);
      }
    );
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
