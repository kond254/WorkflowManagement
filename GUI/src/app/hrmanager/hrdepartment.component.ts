import { Component, ViewChild } from '@angular/core';
import candidateData from '../../assets/candidates.json';


@Component({
  selector: 'app-hrdepartment',
  templateUrl: './hrdepartment.component.html',
  styleUrl: './hrdepartment.component.css',
  
})

export class HrdepartmentComponent{
  name:string ='';
  education:string ='';
  location:string ='';
  salary:number = 0;
  age:number = 0;
  info:string ='';
  step = 0;


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
  candidates: { name: string; education: string; location: string; salary: number; age: number; info: string }[] = candidateData;

  //Funktion speichert die Benutzer eingaben
  saveData(): void {
    const newData = {
      name: this.name,
      education: this.education,
      location: this.location,
      salary: this.salary,
      age: this.age,
      info: this.info,
    };

    // hier neuen Daten in Array
    this.candidates.push(newData);
    console.log('Saved data local.');

    this.name = '';
    this.education = '';
    this.location = '';
    this.salary = 0;
    this.age = 0;
    this.info = '';
  }

}