import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
// import candidateData from '../../assets/candidates.json';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
import { DataServiceInterface } from '../data.service';
import { AfterContentChecked } from '@angular/core';

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

export class HrdepartmentComponent implements OnInit, AfterContentChecked{

  jobOffer: JobOffer = {
    processID: 0,
    professionTitel: '',
    professionType: '',
    numberProfessions: 0,
    description: ''
  };

  dataJobStandards: JobStandards[]=[];
  dataJobOffer: JobOffer[]=[];
  dataJobOfferAccepted: JobOffer[]=[];
  dataTopCandidate: TopCandidate[]=[];
  dataNewEmployees: NewEmployees[]=[];

  stepJO = 0;
  stepJS = 0;
  stepTC= 0;
  stepNE = 0;

  constructor(private dataService: DataMessageService, private snackbarService: SnackbarService,private dataServiceInterface: DataServiceInterface, private cdRef: ChangeDetectorRef) {}

  ngAfterContentChecked(): void {
    this.cdRef.detectChanges();
  }

  async ngOnInit(): Promise<any> {
    await this.getJobOffer();
    await this.getJobOfferAccepted();
    await this.getjobStandards();
    await this.getTopCandidate();
    await this.getnewEmployees();  
  }


  //Funktion ruft alle neuen job offer vom DataServiceInterface ab
  getJobOffer() {
    this.dataServiceInterface.getJobOffer().subscribe(
      data => {
        this.dataJobOffer = data as JobOffer[];
        console.log("Data job offer retrieved");
        console.log(this.dataJobOffer);
      },
      error => {
        console.log("Error fetching job offer data");
        console.log(this.dataJobOffer);
      }
    );
  }

  //Funktion ruft alle akzeptierten job offer vom DataServiceInterface ab
  getJobOfferAccepted() {
    
    this.dataServiceInterface.getJobOfferAccepted().subscribe(
      data => {
        this.dataJobOfferAccepted = data as JobOffer[];
        console.log("Data accepted job offer retrieved");
      },
      error => {
        console.log("Error fetching accepted job offer data");
      }
    );
  }

  //Funktion ruft alle job standards vom DataServiceInterface ab
  getjobStandards(){
    this.dataServiceInterface.getJobStandards().subscribe(
      data => {
        this.dataJobStandards = data as JobStandards[];
        console.log("Data job standards retrieved");
      },
      error => {
        console.log("Error fetching job standards data");
      }
    );
  }

  //Funktion ruft alle neuen top candidates vom DataServiceInterface ab
  getTopCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.dataTopCandidate = data as TopCandidate[];
        console.log("Data top candidates retrieved");
      },
      error => {
        console.log("Error fetching top candidate data");
      }
    );
  }
  //Funktion ruft alle new employees vom DataServiceInterface ab
  getnewEmployees(){
    this.dataServiceInterface.getNewEmployees().subscribe(
      data => {
        this.dataNewEmployees = data as NewEmployees[]; 
        console.log("Data new employees retrieved");
      },
      error => {
        console.log("Error fetching new employee data");
      }
    );
  }
  
  
  //Funktion sendet neuen Job Offer ans DataServiceInterface
  sendData() {
    this.dataServiceInterface.sendJobOffer(this.jobOffer).subscribe(
      response => {
        console.log('Data job offer sent successfully', response);
        this.snackbarService.showSuccess('New job offer sented');
        this.getJobOffer();
      },
      error => {
        console.log('Error sending job offer data');
      }
    );
  }


  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepJO(index: number) {
    this.stepJO = index;
  }
  nextStepJO() {
    this.stepJO++;
  }
  prevStepJO() {
    this.stepJO--;
  }

  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepJS(index: number) {
    this.stepJS = index;
  }
  nextStepJS() {
    this.stepJS++;
  }
  prevStepJS() {
    this.stepJS--;
  }

  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepTC(index: number) {
    this.stepTC = index;
  }
  nextStepTC() {
    this.stepTC++;
  }
  prevStepTC() {
    this.stepTC--;
  }

  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepNE(index: number) {
    this.stepNE = index;
  }
  nextStepNE() {
    this.stepNE++;
  }
  prevStepNE() {
    this.stepNE--;
  }

}
