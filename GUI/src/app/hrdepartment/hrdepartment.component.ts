import { Component, ViewChild } from '@angular/core';
import { MatAccordion } from '@angular/material/expansion';

@Component({
  selector: 'app-hrdepartment',
  templateUrl: './hrdepartment.component.html',
  styleUrl: './hrdepartment.component.css',
  
})

export class HrdepartmentComponent {
  // @ViewChild(MatAccordion) accordion: MatAccordion;
  step = 0;

  setStep(index: number) {
    this.step = index;
  }

  nextStep() {
    this.step++;
  }

  prevStep() {
    this.step--;
  }



  // openAll() {
  //   this.accordion.openAll();
  // }

  // closeAll() {
  //   this.accordion.closeAll();
  // }

}