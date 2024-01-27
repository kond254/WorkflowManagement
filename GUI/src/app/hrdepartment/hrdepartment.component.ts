import { Component, OnInit } from '@angular/core';
import candidateData from '../../assets/candidates.json';
import { DataService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
/*
*
*
*/
import { DataServiceTest } from '../data.service';

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
  graduactionLevel:string ='';
  location:string ='';
  salary: string ='';
  numberEmployees: string ='';
  info:string ='';
  data: Candidate[]=[];
  

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

  constructor(private dataService: DataService, private snackbarService: SnackbarService,private dataServiceTest: DataServiceTest) {}

  async ngOnInit(): Promise<any> {
    this.getCandidate();
    console.log(this.getCandidate());
  }

  async getCandidate() {
    return new Promise((resolve, reject) => {
      this.dataServiceTest.getTopCandidate().subscribe(data => {
        console.log("Test");
        console.log(data)
        resolve(data);
      }, error => {
        reject(error);
      });
    });
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
  async fetchData() {
    try {
      const data = await this.getCandidate(); // Wait for the data to be fetched
      this.data = data as Candidate[]; // Assign the data to this.data, casting it to Candidate[]
    } catch (error) {
      console.error("Error fetching candidate data:", error);
    }
  }
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
    const newData = {
      professionTitel: this.professionTitel,
      professionType: this.professionType,
      graduactionLevel: this.graduactionLevel,
      location: this.location,
      salary: this.salary,
      numberEmployees: this.numberEmployees,
      info: this.info,
    };
    console.log(newData)
  
  // hier neuen Daten in Array
  this.newjobOffer.push(newData);
  // this.dataService.saveData(newData);

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

}
