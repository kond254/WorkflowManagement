import { Component } from '@angular/core';
import jobinformationData from '../../assets/jobinformation.json';

@Component({
  selector: 'app-hrmanager',
  templateUrl: './hrmanager.component.html',
  styleUrl: './hrmanager.component.css'
})
export class HrmanagerComponent {
  jobtitle:string ='';
  number:string = '';
  location:string ='';
  salary:number = 0;
  additionalinformation:string ='';
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
  jobinformation: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string }[] = jobinformationData;

  //Funktion speichert die Benutzer eingaben
  saveData(): void {
    const newData = {
      jobtitle: this.jobtitle,
      number: this.number,
      location: this.location,
      salary: this.salary,
      additionalinformation: this.additionalinformation,
    };

    // hier neuen Daten in Array
    this.jobinformation.push(newData);
    console.log('Saved data local.');

    this.jobtitle = '';
    this.number = '';
    this.location = '';
    this.salary = 0;
    this.additionalinformation = '';
  }


  // Funktion, um den Job zu akzeptieren
  acceptJob(item: any): void {
    // hier die Logik zum Akzeptieren des Jobs implmentieren
    console.log('Job accepted:', item);
  }

  // Funktion, um den Job abzulehnen
  rejectJob(item: any): void {
    // hier die Logik zum Ablehnen des Jobs des Jobs implmentieren
    console.log('Job rejected:', item);
  }

}
