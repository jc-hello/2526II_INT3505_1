import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service(#{ title: "Library Management API" })
@server("http://localhost:8000", "Local server")
namespace Library;

model Book {
  @key id: string;
  title: string;
  author: string;
  year?: int32;
  availableCopies: int32;
}

model BookCreate {
  title: string;
  author: string;
  year?: int32;
  availableCopies: int32;
}

model Member {
  @key id: string;
  name: string;
  email: string;
}

model MemberCreate {
  name: string;
  email: string;
}

model Loan {
  @key id: string;
  bookId: string;
  memberId: string;
  status: "BORROWED" | "RETURNED";
  borrowedAt: utcDateTime;
  returnedAt?: utcDateTime;
}

model LoanCreate {
  bookId: string;
  memberId: string;
}

@route("/books")
op listBooks(): Book[];

@route("/books")
@post
op createBook(@body body: BookCreate): Book;

@route("/books/{id}")
op getBook(@path id: string): Book;

@route("/members")
op listMembers(): Member[];

@route("/members")
@post
op createMember(@body body: MemberCreate): Member;

@route("/loans")
@post
op createLoan(@body body: LoanCreate): Loan;

@route("/loans/{id}/return")
@post
op returnLoan(@path id: string): Loan;
