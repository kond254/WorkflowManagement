import { Component } from '@angular/core';
import candidateData from '../../assets/candidates.json';
import { DataService } from '../message.service';
import { SnackbarService } from '../snackbar.service';


@Component({
  selector: 'app-hrdepartment',
  templateUrl: './hrdepartment.component.html',
  styleUrl: './hrdepartment.component.css',
  
})

export class HrdepartmentComponent{
  professionTitel:string ='';
  professionType:string ='';
  graduactionLevel:string ='';
  location:string ='';
  salary: string ='';
  numberEmployees: string ='';
  info:string ='';

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

  constructor(private dataService: DataService, private snackbarService: SnackbarService,) {}

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
  data: { name: string; education: string; location: string; salary: number; age: number; info: string }[] = candidateData;

  //Funktion prüft, ob candiates leer
  hasData(): boolean {
    return this.data.some(data =>
      data.name.trim() !== '' &&
      data.education.trim() !== '' &&
      data.location.trim() !== '' &&
      data.info.trim() !== '' &&
      data.salary  !== 0 &&
      data.age  !== 0 &&
      data.info.trim()
    );
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
