import { Component, OnInit } from '@angular/core';
import { SnackbarService } from '../snackbar.service';
import { DataServiceInterface } from '../data.service';
import { SocketService } from '../socket.service';

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

// interface Candidate {
//   CandidateID: number;
//   ProcessID: number;
//   address: string;
//   age: number;
//   city: string;
//   country: string;
//   email: string;
//   first_name: string;
//   gender: string;
//   last_name: string;
//   linkedin: string;
//   previous_company: string;
//   rating: number;
//   zip_code: string;
// }

//This interface defines the structure of the JobOffer Object
interface JobOffer {
  description: string;
  numberProfessions: number;
  processID: number;
  professionTitel: string;
  professionType: string;
  hrmanagerAccepted: boolean;
  jobStandardSent: boolean;
}

//This interface defines the structure of the TopCandidate Object
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

//This interface defines the structure of the JobStandardsWithTopCandidates Object
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
// datacandidate: Candidate[]=[];  
dataTopCandidate: TopCandidate[]=[];
dataJobStandardsWithTopCandidates: JobStandardsWithTopCandidates []=[];

newjobStandards: {
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
  numberOfPositions: number
}[] = [];

// These variables are used to control progress within the user interface
step = 0;
candidateSteps=0;
jobStandardSteps = 0

// This structure initiates the four different services: DataMessageService, SnackbarService, DataServiceInterface and SocketService
constructor(private snackbarService: SnackbarService,private dataServiceInterface: DataServiceInterface, private socketService: SocketService) {}

// In this method, various functions are called to load data.
  async ngOnInit(): Promise<any> {
    // await this.getCandidate();
    await this.getJobOffer();
    await this.getjobStandards();
    await this.getJobOfferAccapted();
    await this.getTopCandidate();

// Used to execute getJobOffer when JobOfferUpdated is executed in order to automatically display a new JobOffer in the HRManager when it is created in the HrDepartment without manually reloading the HrManager page
    this.socketService.onJobOfferUpdated().subscribe(() => {
      this.getJobOffer();
    });
  }


  // async getCandidate() { 
  //   this.dataServiceInterface.getTopCandidate().subscribe(
  //     data => {
  //       this.datacandidate = data as Candidate[];
  //       console.log(this.datacandidate)
  //     },
  //     error => {
  //       console.error("Error fetching candidate data:", error);
  //     }
  //   );
  // }

  // The getJobOfferAccapted() method retrieves the job offers already accapted by the HrManager via the DataServiceInterface and stores it in dataJobOfferAccapted
  async getJobOfferAccapted() {
    this.dataServiceInterface.getJobOfferAccepted().subscribe(
      data => {
        this.dataJobOfferAccapted = data as JobOffer[];
        console.log(this.dataJobOfferAccapted)
      },
      error => {
        console.error("Error fetching candidate data:", error);
      }
    );
  }

  // The getjobStandards() method retrieves the job standards via the DataServiceInterface and stores it in dataJobStandards
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

  // The getJobOffer() method retrieves the job offers created by the HrDepartment via the DataServiceInterface and stores it in dataJobOffer
  async getJobOffer() {
    this.dataServiceInterface.getJobOffer().subscribe(
      data => {
        this.dataJobOffer = data as JobOffer[]; 
        console.log(this.dataJobOffer)
      },
      error => {
        console.error("Error fetching job offer data:", error);
      }
    );
  }

// The getTopCandidate method retrieves the top candidates via the DataServiceInterface and stores it in dataJobOffer dataTopCandidate
   async getTopCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.dataTopCandidate = data as TopCandidate[]; 
        console.log(this.dataTopCandidate)
      },
      error => {
        console.error("Error fetching top candidate data:", error);
      }
    );
  } 

// The getJobStandardsWithTopCandidates method uses the DataServiceInterface to retriev the jobStandards and the top candidates with the same ProcessID and saves the result in the dataJobStandardsWithTopCandidates array
  async getJobStandardsWithTopCandidates(jobStandards: JobStandards) {
    console.log(typeof(jobStandards["ProcessID"])) 
    console.log((jobStandards["ProcessID"])) 
    this.dataJobStandardsWithTopCandidates=[];
    this.dataServiceInterface.getJobStandardsWithCandidates(jobStandards["ProcessID"]).subscribe(
      data => {
        this.dataJobStandardsWithTopCandidates = data as JobStandardsWithTopCandidates [];
        console.log(this.dataJobStandardsWithTopCandidates)
      },
      error => {
        console.error("Error fetching JobStandardsWithTopCandidates data:", error);
      }
    );
  }
// This method uses the DataServiceInterface to transfer the job standards, which are entered in the second panel of the hrManager and derived from the ProcessID, JobTitle, JobType and numberOfPositions, from the original Job Offer to the backend
  sendData(currentJobOffer: JobOffer) {
    this.jobStandards.ProcessID = (currentJobOffer.processID); 
    this.jobStandards.JobTitle = (currentJobOffer.professionTitel); 
    this.jobStandards.JobType = (currentJobOffer.professionType); 
    this.jobStandards.numberOfPositions = (currentJobOffer.numberProfessions); 

    
    this.jobStandards.JobMode = this.jobStandards.JobMode.toUpperCase();
    this.jobStandards.Location = this.jobStandards.Location.toUpperCase();


    console.log(this.jobStandards) 
    this.dataServiceInterface.sendJobStandards(this.jobStandards).subscribe(
      response => {
        console.log('Data sent successfully', response);
        this.snackbarService.showSuccess('New job standards sent');
        this.jobStandards = {} as JobStandards;
       
      },
      error => {
        console.error('Error sending data', error);
        
      }

    );

  }

  // These methods set the number for the Previous Next function
  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }

  // These methods set the number for the Previous Next function in the top candidate cards
  setStepCandidates(index: number) {
    this.candidateSteps = index;
  }

  nextStepCandidates() {
    this.candidateSteps++;
  }

  prevStepCandidates() {
    this.candidateSteps--;
  }

// These methods set the number for the Previous Next function in the job standards card
  setStepJobStandard(index: number){
    this.jobStandardSteps = index;
  }

  nextStepJobStandard() {
    this.step++;
  }

  prevStepJobStandard() {
    this.step--;
  }

  

// This method is called when the accept button on the HrManager page is pressed for the job offer. It sets the hrmanagerAccepted status of the job offer to true and then calls the updateJobOffer method.
  acceptJob(item: JobOffer): void {
    console.log('Job accepted:', item);
    item.hrmanagerAccepted = true;
    this.updateJobOffer(item);
  }

  // This method is called when the reject button on the HrManager page is pressed for the job offer. It calls the deletJobOffer method.
  rejectJob(item: JobOffer): void {
    console.log('Job rejected:', item);
    this.deleteJobOffer(item);
  }

updateJobOffer(item: JobOffer): void {
  this.dataServiceInterface.updateJobOffer(item).subscribe(
    response => {
      console.log('Job offer updated successfully', response);
      this.snackbarService.showSuccess('Job offer accepted');
      this.getJobOffer();
      this.getJobOfferAccapted();
    },
    error => {
      console.error('Error updating job offer', error);
    }
  );
}

updateJobOfferAfterSend(item: JobOffer): void {
  this.dataServiceInterface.updateJobOfferAfterSend(item).subscribe(
    response => {
      console.log('Job offer updated successfully', response);
      this.snackbarService.showSuccess('Job offer accepted');
      this.getJobOfferAccapted();
    },
    error => {
      console.error('Error updating job offer', error);
    }
  );
}



deleteJobOffer(item: JobOffer): void {
  this.dataServiceInterface.deleteJobOffer(item).subscribe(
    response => {
      console.log('Job offer delete successfully', response);
      this.snackbarService.showSuccess('Job offer rejected');
      this.getJobOffer();
      this.getJobOfferAccapted();
    },
    error => {
      console.error('Error delete job offer', error);
    }
  );
}

acceptTopCandidate(item: JobStandardsWithTopCandidates, jobStandards: JobStandards): void {
  console.log('Top candidate accepted:', item);
  item.hrmanagerAccepted = true; 
  this.dataServiceInterface.updateTopCandidate(item).subscribe(
    response => {
      console.log('Top candidate updated successfully', response);
      this.snackbarService.showSuccess('Top candidate accepted');
      this.getJobStandardsWithTopCandidates(jobStandards);
    },
    error => {
      console.error('Error updating top candidate', error);
    }
  );
 
}

rejectTopCandidate(item: JobStandardsWithTopCandidates, jobStandards: JobStandards): void {
  console.log('Top candidate rejected:', item);
  this.dataServiceInterface.deleteTopCandidate(item).subscribe(
    response => {
      console.log('Top candidate delete successfully', response);
      this.snackbarService.showSuccess('Top candidate rejected');
      this.getJobStandardsWithTopCandidates(jobStandards);
    },
    error => {
      console.error('Error delete Top Candidate', error);
    }
  );
}
}
