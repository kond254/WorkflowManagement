import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


interface DataRoleServiceService {

  [key: string]: {
    home: boolean;
    hrdepartment: boolean;
    hrmanagement: boolean;
    accounting: boolean;
  };
}

@Injectable({
  providedIn: 'root',
})

// This class allows to read the rights of the users from the roleData.json and other components can set and retrieve the individual page rights as boolean
export class DataRoleService {

  private home: boolean = false;
  private hrdepartment: boolean = false;
  private hrmanagement: boolean = false;
  private accounting: boolean = false;
  private apiUrl = 'assets/roleData.json';

  constructor(private http: HttpClient) {}

  
  //Function that retrieve the boolean values of the respective role rights from the roleData.json
  getRoleData(role: string): Observable<DataRoleServiceService> {
    return this.http.get<DataRoleServiceService>(this.apiUrl);
  }

  //Function to get the boolean value from the home page right
  get showRoleHome(): boolean {
    return this.home;
  }

  //Function to set the boolean value from the home page right
  set showRoleHome(value: boolean) {
    this.home = value;
  }

  //Function to get the boolean value from the hrdepartment page right
  get showRoleHrdepartment(): boolean {
    return this.hrdepartment;
  }

  //Function to set the boolean value from the hrdepartment page right
  set showRoleHrdepartment(value: boolean) {
    this.hrdepartment = value;
  }

  //Function to get the boolean value from the hrmanagement page right
  get showRoleHrmanagement(): boolean {
    return this.hrmanagement;
  }

  //Function to set the boolean value from the hrmanagement page right
  set showRoleHrmanagement(value: boolean) {
    this.hrmanagement = value;
  }

  //Function to get the boolean value from the accounting page right
  get showRoleAccouting(): boolean {
    return this.accounting;
  }

  //Function to set the boolean value from the ccounting page right
  set showRoleAccouting(value: boolean) {
    this.accounting = value;
  }
  
  //Function that other components call to set the boolean value from the home, hrdepartment, hrmanagement and accounting page right
  updateRoles(showRoleHome: boolean, showRoleHrdepartment: boolean, showRoleHrmanagement: boolean, howRoleAccouting: boolean): void {
    this.home = showRoleHome;
    this.hrdepartment = showRoleHrdepartment;
    this.hrmanagement = showRoleHrmanagement;
    this.accounting = howRoleAccouting;
  }
}