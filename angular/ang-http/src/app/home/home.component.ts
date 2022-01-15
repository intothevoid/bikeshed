import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { DataService } from '../data.service';
import { takeUntil } from 'rxjs';

interface Product {
  id: number;
  name: string;
  description: string;
  price: string;
  imageUrl: string;
  quantity: number;
}

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
  products: Product[] = [];
  destroy$: Subject<boolean> = new Subject<boolean>();

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService
      .sendGetRequest()
      .pipe(takeUntil(this.destroy$))
      .subscribe((data: any) => {
        console.log(data);
        this.products = data;
      });
  }

  ngOnDestroy() {
    this.destroy$.next(true);

    // Unsubscribe from the subject
    this.destroy$.unsubscribe();
  }
}
