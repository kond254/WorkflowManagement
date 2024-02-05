import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { SnackbarService } from '../snackbar.service';
import { DataServiceInterface } from '../data.service';
import { AfterContentChecked } from '@angular/core';
import { SocketService } from '../socket.service';
import { DialogService } from '../dialog.service';

//This interface defines the structure of the JobStandards Object
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

//This interface defines the structure of the Contract Object
interface Contract{
  ProcessID: number,
  numberProfessions: number,
  suggestion: number,
  compensation: number,
  professionType: string
}

//This interface defines the structure of the TopCandidateAccepted Object
interface TopCandidateAccepted {
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
  InterviewDate: Date;
}

//This interface defines the structure of the JobOffer Object
interface JobOffer {
  description: string;
  numberProfessions: number;
  processID: number;
  professionTitel: string;
  professionType: string;
}
//This interface defines the structure of the NewEmployees Object
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

  // exampleContract: Contract = {
  //   ProcessID: 1,
  //   numberProfessions: 3,
  //   suggestion: 123,
  //   compensation: 5000,
  //   professionType: 'Engineer',
  // };

  percentage: number = 0;

  dataJobStandards: JobStandards[]=[];
  dataJobOffer: JobOffer[]=[];
  dataJobOfferAccepted: JobOffer[]=[];
  dataTopCandidateAccepted: TopCandidateAccepted[]=[];
  dataNewEmployees: NewEmployees[]=[];
  dataContract: Contract[]=[];

  // These variables are used to control progress within the user interface
  stepJO = 0;
  stepJS = 0;
  stepTC= 0;
  stepNE = 0;
  stepCO = 0;

  // This structure initiates the six different services: DataMessageService, SnackbarService, DataServiceInterface, ChangeDetectorRef,   SocketService and DialogService 
  constructor(private snackbarService: SnackbarService,private dataServiceInterface: DataServiceInterface, private cdRef: ChangeDetectorRef, private socketService: SocketService, private dialogService: DialogService) {}

  ngAfterContentChecked(): void {
    this.cdRef.detectChanges();
  }

  // In this method, various functions are called to load data.
  async ngOnInit(): Promise<any> {
    await this.getJobOffer();
    await this.getJobOfferAccepted();
    await this.getjobStandards();
    await this.getTopCandidate();
    await this.getnewEmployees();  
    await this.getCurrentContractSuggestions();

    // Used to execute getJobOffer and getJobOfferAccepted when JobOfferUpdated is executed in order to automatically display new JobOffer and accepted job offers in the HRDepartment when the HrManager accepts a job offer without manually reloading the HrDepartment page
    this.socketService.onJobOfferUpdated().subscribe(() => {
      this.getJobOffer();
      this.getJobOfferAccepted();
    });

    // Used to execute getJobOffer and getJobOfferAccepted when JobOfferAcceptedUpdated is executed in order to automatically display new job fffer and accepted job offers in the HRDepartment when the HrManager accepts a job offer without manually reloading the HrDepartment page
    this.socketService.onJobOfferAcceptedUpdated().subscribe(() => {
      this.getJobOffer();
      this.getJobOfferAccepted();
    });

    // Used to execute getjobStandards when JobStandardsUpdated is executed in order to automatically display new job standard the HRDepartment when the HrManager creats a new job standard without manually reloading the HrDepartment page
    this.socketService.onJobStandardsUpdated().subscribe(() => {
      this.getjobStandards();
    });

    // Used to execute getTopCandidate when TopCandidatesAcceptedUpdated is executed in order to automatically display new top candidates in the HRDepartment without manually reloading the HrDepartment page
    this.socketService.onTopCandidatesAcceptedUpdated().subscribe(() => {
      this.getTopCandidate();
    });
    
    // this.dataContract.push(this.dataContract[]); 
    
  }

  // The getJobOffer() method retrieves the job offers created by the HrDepartment via the DataServiceInterface and stores it in dataJobOffer
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

  // The getJobOfferAccapted() method retrieves the job offers already accapted by the HrManager via the DataServiceInterface and stores it in dataJobOfferAccapted
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

  // The getjobStandards() method retrieves the job standards via the DataServiceInterface and stores it in dataJobStandards
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

  // The getCurrentContractSuggestions() method retrieves current contract suggestions via the DataServiceInterface and saves them in dataContract.
  getCurrentContractSuggestions() {
    this.dataServiceInterface.getCurrentSuggestions().subscribe(
      data => {
        // this.exampleContract;
        this.dataContract = data as Contract[];
        console.log("Data accepted contracts retrieved");
      },
      error => {
        console.log("Error fetching accepted contracts data");
      }
    );
  }

  // The getTopCandidate method retrieves the top candidates via the DataServiceInterface and stores it in dataJobOffer dataTopCandidate
  getTopCandidate() {
    this.dataServiceInterface.getTopCandidateAccepted().subscribe(
      data => {
        this.dataTopCandidateAccepted = data as TopCandidateAccepted[];
        console.log("Data accepted top candidates retrieved");
      },
      error => {
        console.log("Error fetching accepted top candidate data");
      }
    );
  }

  // The getnewEmployees method retrieves the new Employees via the DataServiceInterface and stores it in dataNewEmployees
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
  
  

  // This method uses the DataServiceInterface to transfer the job offers, which are entered in the first panel of the hrdepartment to the backend
  sendData() {
    
    this.jobOffer.professionType = this.jobOffer.professionType.toUpperCase();

    this.dataServiceInterface.sendJobOffer(this.jobOffer).subscribe(
      response => {
        console.log('Data job offer sent successfully', response);
        this.snackbarService.showSuccess('New job offer sent');
        this.jobOffer = {} as JobOffer;
      },
      error => {
        console.log('Error sending job offer data');
      }
    );
  }


   //The openDialogPay(contract: Contract) method is used to submit an offer via a the DataServiceInterface
   openDialogPay(contract: Contract): void {
    console.log(contract);
    this.dataServiceInterface.postCurrentContractSuggestion(contract).subscribe(
      response => {
        console.log('Contract offer sent successfully', response);
        this.snackbarService.showSuccess('Contract sent');
      },
      error => {
        console.log('Error sending Contract');
      }
    );
  }


  // These methods set the number for the Previous Next function in the job offer card
  setStepJO(index: number) {
    this.stepJO = index;
  }
  nextStepJO() {
    this.stepJO++;
  }
  prevStepJO() {
    this.stepJO--;
  }

  // These methods set the number for the Previous Next function in the job standards card
  setStepJS(index: number) {
    this.stepJS = index;
  }
  nextStepJS() {
    this.stepJS++;
  }
  prevStepJS() {
    this.stepJS--;
  }

  // These methods set the number for the Previous Next function in the top candidates card
  setStepTC(index: number) {
    this.stepTC = index;
  }
  nextStepTC() {
    this.stepTC++;
  }
  prevStepTC() {
    this.stepTC--;
  }

  // These methods set the number for the Previous Next function in the new employee card
  setStepNE(index: number) {
    this.stepNE = index;
  }
  nextStepNE() {
    this.stepNE++;
  }
  prevStepNE() {
    this.stepNE--;
  }

  // Funktion setzt die Nummer des Pannels, für die Funktion Zurück/Vor
  setStepCO(index: number) {
    this.stepNE = index;
  }
  nextStepCO() {
    this.stepNE++;
  }
  prevStepCO() {
    this.stepNE--;
  }

}
