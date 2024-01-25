import { Component } from '@angular/core';
import jobinformationData from '../../assets/jobinformation.json';
import { DataService } from '../message.service';
import { SnackbarService } from '../snackbar.service';
import candidateData from '../../assets/candidates.json';
import jobinformationacceptedData from '../../assets/jobinformationaccepted.json';


@Component({
  selector: 'app-hrmanager',
  templateUrl: './hrmanager.component.html',
  styleUrl: './hrmanager.component.css'
})
export class HrmanagerComponent {
  professionTitel:string ='';
  professionType:string ='';
  graduactionLevel:string ='';
  location:string ='';
  salary: string ='';
  numberEmployees: string ='';
  info:string ='';

  jobtitle:string ='';
  number:string = '';
  additionalinformation:string ='';

  id: string ='';
  

  dataNews: any[] = [];

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

  newjobInformation: {
    jobtitle: string;
    number: string;
    location: string;
    salary: number;
    additionalinformation: string;
  }[] = jobinformationData;

  newjobinformationaccepted: {
    jobtitle: string;
    number: string;
    location: string;
    salary: number;
    additionalinformation: string;
    id: string;
  }[] = jobinformationacceptedData;


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
  dataCandidate: { name: string; education: string; location: string; salary: number; age: number; info: string }[] = candidateData;
  dataJobInformation: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string }[] = jobinformationData;
  dataJobInformationAccepted: { jobtitle: string; number: string; location: string; salary: number; additionalinformation: string; id: string }[] = jobinformationacceptedData;
 




  //Funktion prüft, ob candiates leer
  hasData(): boolean {
    return this.dataCandidate.some(data =>
      data.name.trim() !== '' &&
      data.education.trim() !== '' &&
      data.location.trim() !== '' &&
      data.info.trim() !== '' &&
      data.salary  !== 0 &&
      data.age  !== 0 &&
      data.info.trim()
    );
  }

    //Funktion prüft, ob Job Information leer

  hasJobInformation(): boolean {
    return this.dataJobInformation.some(data =>
      data.jobtitle.trim() !== '' &&
      data.number.trim() !== '' &&
      data.location.trim() !== '' &&
      data.additionalinformation.trim() !== '' &&
      data.salary !== 0
    );
  }

  hasJobInformationAccepted(): boolean {
    return this.dataJobInformationAccepted.some(data =>
      data.jobtitle.trim() !== '' &&
      data.number.trim() !== '' &&
      data.location.trim() !== '' &&
      data.additionalinformation.trim() !== '' &&
      data.id.trim() !== '' &&
      data.salary !== 0
    );
  }
  isValidForm(): boolean {
    return !(!this.professionTitel || !this.professionType || !this.graduactionLevel || !this.location || !this.salary || !this.numberEmployees);
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



  this.snackbarService.showSuccess('New job information saved');
  this.resetJobInfoInputFields();

  }

      // Funktion speichert die Benutzereingabe
  saveJobInformation(): void {
    const newJobInfo = {
      jobtitle: this.professionTitel,
      number: this.numberEmployees,
      location: this.location,
      salary: parseFloat(this.salary),
      additionalinformation: this.info,
    };

  this.newjobInformation.push(newJobInfo);
    
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

  resetJobInfoInputFields(): void {
    this.professionTitel = '';
    this.numberEmployees = '';
    this.location = '';
    this.salary = '';
    this.info = '';
  }

  resetJobInfoAcceptedInputFields(): void {
    this.professionTitel = '';
    this.numberEmployees = '';
    this.location = '';
    this.salary = '';
    this.info = '';
    this.id = ''; 
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
