import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root',
})
export class RoleService {
  private home: boolean = false;
  private hrdepartment: boolean = false;
  private hrmanagement: boolean = false;
  private accounting: boolean = false;

  get showRoleHome(): boolean {
    return this.home;
  }

  set showRoleHome(value: boolean) {
    this.home = value;
  }

  get showRoleHrdepartment(): boolean {
    return this.hrdepartment;
  }

  set showRoleHrdepartment(value: boolean) {
    this.hrdepartment = value;
  }

  get showRoleHrmanagement(): boolean {
    return this.hrmanagement;
  }

  set showRoleHrmanagement(value: boolean) {
    this.hrmanagement = value;
  }

  get showRoleAccouting(): boolean {
    return this.accounting;
  }

  set showRoleAccouting(value: boolean) {
    this.accounting = value;
  }
  updateRechte(showRoleHome: boolean, showRoleHrdepartment: boolean, showRoleHrmanagement: boolean, howRoleAccouting: boolean): void {
    this.home = showRoleHome;
    this.hrdepartment = showRoleHrdepartment;
    this.hrmanagement = showRoleHrmanagement;
    this.accounting = howRoleAccouting;
  }
}
