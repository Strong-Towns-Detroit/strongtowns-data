// lib.typ — single import surface for the publication library.
//
//   #import "../lib/lib.typ": *
//
// Everything a template or issue document needs is re-exported here so that
// document sources never reach into individual modules.

#import "theme.typ": *
#import "status.typ": *
#import "callouts.typ": *
#import "tables.typ": *
#import "sources.typ": *
#import "appendix.typ": *
#import "doc.typ": *
