import { Component, OnInit } from '@angular/core';
import candidateData from '../../assets/candidates.json';
import { DataMessageService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
/*
*
*
*/
import { DataServiceInterface } from '../data.service';

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


@Component({
  selector: 'app-hrdepartment',
  templateUrl: './hrdepartment.component.html',
  styleUrl: './hrdepartment.component.css',
  
})

export class HrdepartmentComponent implements OnInit {
  professionTitel:string ='';
  professionType:string ='';
  numberProfessions: number = 0;
  discription:string ='';
  data: Candidate[]=[];
  

  /// newjobOffer: JobOffer[] = [];

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
    // await this.sendJobOffer();
  }

  async getCandidate() {
    this.dataServiceInterface.getTopCandidate().subscribe(
      data => {
        this.data = data as Candidate[]; // Assign the data to this.data
        console.log(this.data)
      },
      error => {
        console.error("Error fetching candidate data:", error);
      }
    );
  }

  // Hier ist die neue send funktion
  // sendData(){
  //   dataServiceInterface.sendJobOffer(candidateData).subscribe(response => {
  //     console.log('Response from sendCandidate:', response);
  //   });
  // }
  


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
  saveData(): void {
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

  this.snackbarService.showSuccess('New job offer sent');
  this.resetInputFields();
    
  }

  resetInputFields():void{
    this.professionTitel = '';
    this.professionType = '';
    this.numberProfessions = 0;
    this.discription = '';
  }

}
